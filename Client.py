import socket
import time

HOST = "192.168.1.107"
PORT = 9000

server_info = (HOST, PORT)
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock.connect(server_info)
print("TCP Connection Established\n")
msg = ''
while True:
    print("------------------------------------------------------")
    print("You will pass the message to the server line by line")
    print("------------------------------------------------------")
    while True:
        print("Please enter the line you want to pass to the server")
        print("If this is the last line, enter -1")
        raw_input = input()
        if raw_input == '-1':
            break
        if msg == '':
            msg = raw_input
        else:
            msg = msg + '\n' + raw_input
    print('sending:\n' + msg)
    byte_msg = msg.encode()
    sock.send(byte_msg)
    msg = ''
    data = sock.recv(1024)
    print('received:\n' + data.decode())
    print("Would you like to kill this session? (y or n)")
    answer = input()
    if answer == 'y':
        sock.send("KILL".encode())
        break
print("Closing connection...")
sock.close()
