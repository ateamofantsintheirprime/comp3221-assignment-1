import socket
ip = "127.0.0.1"
port = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print ("message:", data)
