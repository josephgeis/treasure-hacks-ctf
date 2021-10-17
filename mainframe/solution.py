import socket

# Creates socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connects to server
s.connect(("b.ctf.treasurehacks.dev", 9648))

# Receives problem
p = s.recv(128).decode("ascii")

# Evaluates problem, sends answer
s.send(str(eval(p)).encode("ascii"))

# Receives flag
f = s.recv(128)

print(f.decode("ascii"))
