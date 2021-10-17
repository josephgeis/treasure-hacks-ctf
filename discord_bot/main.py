import asyncio
from datetime import datetime
from pytz import timezone
from types import coroutine
import discord
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import desc
import config
import db
import jinja2
import re

env: jinja2.Environment


def render_template(name, **context):
    template = env.get_template(name)
    return template.render(**context)


def admin_command(f):
    async def fail(self, message: discord.Message):
        reply = await message.reply("You can't use this command.")
        await message.delete(delay=5.0)
        await reply.delete(delay=5.0)

    async def wrapper(self, message: discord.Message):
        if message.author.id in config.ADMIN_IDS:
            await f(self, message)
        else:
            await fail(self, message)
            print("fail")

    return wrapper


class CTFClient(discord.Client):
    # MARK: Lifecycle

    async def on_ready(self):
        print(
            f"Successfully connected to Discord as {self.user.name}#{self.user.discriminator}")

    async def on_message(self, message: discord.Message):
        if message.author is self.user:
            return

        if message.content.startswith('\\flag'):
            if message.channel.type is not discord.ChannelType.private:
                await message.delete()
                await message.author.send("Please do not send flags in public channels.")
            else:
                await self.process_flag(message)
        elif message.content.startswith('\\') and len(message.content[1:]) > 0:
            command = message.content[1:].split()[0]
            cmd = self.get_command(command)
            await cmd(message)

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member is self.user:
            return

        if (channel := after.channel) \
            and channel.id == config.TARGET_VOICE_CHANNEL \
                and not self.voice_clients:
            await self.play_ctf_audio(channel)

    # MARK: Helpers
    async def process_flag(self, message: discord.Message):
        if message.channel.type is not discord.ChannelType.private:
            await message.delete()
            warning_message = await message.channel.send(f"<@{message.author.id}> Do not put flags in public chats. Please DM them to <@{self.user.id}>.")
            warning_dm = await message.author.send("Do not put flags in public channels. Please DM them here.")
            return

        flag_txt: None

        if (flag_match := re.match(r"\\flag\{(.+)\}", message.content)) is None \
                or (flag_txt := flag_match.group(1)) is None:
            await message.author.send("Invalid flag.")
            return

        user = message.author
        db_user: db.User
        db_flag: db.Flag
        session = self.Session()

        # * Process flag
        if (db_user := session.query(db.User).filter_by(id=user.id).first()) is None:
            await user.send("I don't know you. Make sure to join before using this command.")
            return

        if db_user.current_flag is None:
            return

        if (db_flag := session.query(db.Flag).filter_by(id=db_user.current_flag).first()) is None:
            await user.send("There was an issue getting the current flag. Please DM an organizer or CTF Helper.")
            return

        flag_count = session.query(db.Flag).count()

        print(db_flag.flag)
        if db_flag.flag == flag_txt:
            db_redemption = db.Redemption(
                user=db_user.id, flag=db_flag.id, timestamp=datetime.now(), points=db_flag.points_remaining)
            session.add(db_redemption)
            db_flag.points_remaining = max(0, db_flag.points_remaining - 1)
            if db_user.current_hint > 0:
                db_redemption.points = int(db_redemption.points / 2)
            session.commit()

            if db_user.current_flag < flag_count:
                score = await self.calculate_score(user.id)
                await user.send(f"Good work agent! You found another flag and scored {db_redemption.points} point{'s' if db_redemption.points != 1 else ''}. Your current score is {score}.")
                db_user.current_flag += 1
                db_user.current_hint = 0
                session.commit()

                await self.command_clue(message)
            else:
                await user.send("Good work agent! You found the last flag.")
                db_user.current_flag = None
                session.commit()
        else:
            await user.send("Try again! Type `\\clue` to get the clue again or `\\hint` if you're stuck.")

    async def join_user(self, user: discord.User):
        session = self.Session()

        if (db_user := session.query(db.User).filter_by(id=user.id).first()) is None:
            db_user = db.User(id=user.id)
            session.add(db_user)
            await user.send(r"Howdy! Welcome to Treasure CTF. To get your first clue, type `\clue` to get started.")
        else:
            await user.send("Looks like you're already in. DM me to pick up where you left off.")

        session.commit()

    async def play_ctf_audio(self, channel: discord.VoiceChannel):
        if vcc := next((vcc for vcc in self.voice_clients if vcc.guild == channel.guild), None):
            print(vcc)
            vcc.cleanup()
            await vcc.disconnect()

        print("vccv")
        vc: discord.VoiceClient = await channel.connect()
        while vc.is_connected():
            vc.play(discord.FFmpegPCMAudio(
                executable="/usr/bin/ffmpeg", source="./hackme.wav"))
            while vc.is_playing():
                await asyncio.sleep(0.1)
            if not(next((user for user in channel.voice_states.keys() if user != self.user.id), None)):
                await vc.disconnect()

    async def calculate_score(self, user_id: int):
        db_user: db.User
        db_flag: db.Flag
        session = self.Session()

        if (db_user := session.query(db.User).filter_by(id=user_id).first()) is None:
            return

        q = session.query(func.sum(db.Redemption.points).label('points')
                          ).filter_by(user=user_id).first()

        if score := q.points:
            return int(score)

    # MARK: Commands

    @admin_command
    async def command_play(self, message: discord.Message):
        if message.author.id in config.ADMIN_IDS:
            self.loop.create_task(self.play_ctf_audio(
                message.author.voice.channel))

        await message.delete()

    async def command_join(self, message: discord.Message):
        await self.join_user(message.author)
        m = await message.reply("Check your DMs!")
        await message.delete(delay=5)
        await m.delete(delay=5)

    async def command_clue(self, message: discord.Message):
        user = message.author
        db_user: db.User
        db_flag: db.Flag
        session = self.Session()

        if (db_user := session.query(db.User).filter_by(id=user.id).first()) is None:
            await user.send("I don't know you. Make sure to join before using this command.")
            return

        if db_user.current_flag is None:
            return

        if (db_flag := session.query(db.Flag).filter_by(id=db_user.current_flag).first()) is None:
            await user.send("There was an issue getting the current flag. Please DM an organizer or CTF Helper.")
            return

        await user.send(render_template(
            "clue.txt", number=db_flag.id, clue=db_flag.clue))

    async def command_hint(self, message: discord.Message):
        # TODO: \hint

        user = message.author
        db_user: db.User
        db_flag: db.Flag
        session = self.Session()

        if (db_user := session.query(db.User).filter_by(id=user.id).first()) is None:
            await user.send("I don't know you. Make sure to join before using this command.")
            return

        if db_user.current_flag is None:
            return

        if (db_flag := session.query(db.Flag).filter_by(id=db_user.current_flag).first()) is None:
            await user.send("There was an issue getting the current flag. Please DM an organizer or CTF Helper.")
            return

        db_user.current_hint = max(
            db_user.current_hint + 1, len(db_flag.hints))
        session.commit()

        await user.send(render_template(
            "hint.txt", flag_number=db_flag.id, clue=db_flag.clue, hints=db_flag.hints[0:db_user.current_hint]))

    # TODO: \leaderboard -- admin command
    @admin_command
    async def command_leaderboard(self, message: discord.Message):
        session = self.Session()

        q = session.query(db.Redemption.user.label('user'), func.sum(
            db.Redemption.points).label('points')).group_by(db.Redemption.user).order_by(desc('points')).limit(5)

        entries = [
            dict(user=r.user, points=r.points)
            for r in q
        ]

        now = datetime.now(tz=timezone("America/Los_Angeles"))

        await message.channel.send(render_template("leaderboard.txt", entries=entries, now=now.strftime("%B %-d, %Y at %-I:%M %p %Z")))

    async def command_not_found(self, message: discord.Message):
        pass

    def get_command(self, name: str) -> coroutine:
        return self.commands.get(name, self.command_not_found)

    def __init__(self, db_uri: str, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.Session = db.create_session(db_uri)

        self.commands = {
            "join:ctf": self.command_join,
            "play": self.command_play,
            "clue": self.command_clue,
            "hint": self.command_hint,
            "leaderboard": self.command_leaderboard
        }


if __name__ == '__main__':
    client = CTFClient(config.DB_URI)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
        autoescape=jinja2.select_autoescape()
    )
    client.run(config.TOKEN)
