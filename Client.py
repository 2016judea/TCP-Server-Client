#Author: Aidan Jude
#Date: 11/26/2018
#Description:
    #This portion of the TCP client/server program is responsible for sending TCP messages
    #and receiving the response from the server. Since the basic function that the server performs is to
    #compute postfix operations, we send messages like so:
        #Example message that is sent => 1428+*+
    #This is equal to 1+(4*(2+8)), so the expected response from the server would be 41

import socket
import time

HOST = "SERVER_IP_ADDRESS"
PORT = 9000 #choose a port number

#utilize the socket library to create a socket object
server_info = (HOST, PORT)
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
#establish a connection with the server
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
        #if the user has no more lines of postfix operation to compute, we terminate the loop
        if raw_input == '-1':
            break
        if msg == '':
            msg = raw_input
        else:
            msg = msg + '\n' + raw_input
    print('sending:\n' + msg)
    #we encode the message to follow the TCP protocol byte format
    byte_msg = msg.encode()
    sock.send(byte_msg)
    msg = ''
    #we read the buffer for the server's response
    data = sock.recv(1024)
    print('received:\n' + data.decode())
    print("Would you like to kill this session? (y or n)")
    answer = input()
    if answer == 'y':
        sock.send("KILL".encode())
        break
print("Closing connection...")
sock.close()
