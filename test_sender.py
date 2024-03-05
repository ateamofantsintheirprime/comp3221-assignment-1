import socket
ip = "127.0.0.1"
port = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"test", (ip, port))
