import socketserver
import random
import select
import time

RECV_TIMEOUT = 20
SOLVE_TIMEOUT = 1


class Puzzle:
    OPERS = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y
    }

    def get_oper(self):
        return Puzzle.OPERS[self.oper]

    def solve(self) -> int:
        oper = self.get_oper()
        return oper(self.x, self.y)

    def __str__(self):
        return f"{self.x} {self.oper} {self.y}"

    def __init__(self):
        self.x = random.randint(6328044, 9568945)
        self.y = random.randint(1328044, 3328043)
        self.oper = ['+', '-', '*'][random.randint(0, 2)]


def get_flag() -> str:
    flag: str
    with open("flag.txt") as fd:
        flag = fd.read()

    return f"Correct! FLAG: {flag}"


class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        puzzle = Puzzle()

        self.request.sendall(f"{puzzle} \n".encode("utf8"))
        print(f"{self.client_address}: {puzzle}")

        ans = None

        data = None

        t1 = time.time()

        ready = select.select([self.request], [], [], RECV_TIMEOUT)
        if ready[0]:
            data = self.request.recv(128).strip()

        t2 = time.time()

        if data is None:
            ans = "timeout"
        else:
            try:
                ans = int(data)
            except ValueError:
                ans = "invalid"

        if ans == "invalid":
            self.request.sendall(b"Invalid response\n")
        elif ans == "timeout":
            self.request.sendall(b"Too slow\n")
        elif ans != puzzle.solve():
            self.request.sendall(b"Incorrect answer\n")
        else:
            if t2 - t1 > SOLVE_TIMEOUT:
                self.request.sendall(b"Too slow\n")
            else:
                self.request.sendall(f"{get_flag()}\n".encode("utf8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9648

    with socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler) as server:
        print(f"Serving on {HOST}:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
