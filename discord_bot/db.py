from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, BigInteger, String, Text, create_engine, DateTime, JSON
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()


class Flag(Base):
    __tablename__ = 'flags'

    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    clue = Column(Text)
    hints = Column(JSON)
    flag = Column(String(64), nullable=False, unique=True)
    points_remaining = Column(Integer, default=20)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    current_flag = Column(Integer, ForeignKey('flags.id'), default=1)
    current_hint = Column(Integer, default=0)
    total_hints = Column(Integer, default=0)
    last_attempt = Column(DateTime)


class Redemption(Base):
    __tablename__ = 'redemptions'

    id = Column(Integer, primary_key=True)
    user = Column(BigInteger, ForeignKey('users.id'))
    flag = Column(Integer, ForeignKey('flags.id'))
    points = Column(Integer)
    timestamp = Column(DateTime)


def create_session(uri: str, eargs=(), ekwargs={}):
    engine = create_engine(uri, *eargs, **ekwargs)
    Session = sessionmaker(bind=engine)

    return Session


def sync(uri: str):
    engine = create_engine(uri, echo=True)
    Base.metadata.create_all(engine)
