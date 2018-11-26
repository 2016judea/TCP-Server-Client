#Author: Aidan Jude
#Date: 11/26/2018
#Description:
    #This portion of the TCP client/server program is responsible for receiving TCP messages
    #and sending the appropriate response. 

import socket
import time

#this function handles the postfix computation by utilizing a list like that of a stack
def eval_postfix(eval_line):
    s = list()
    for symbol in eval_line:
        plus = None
        if symbol in "0123456789":
            s.append(int(symbol))
        elif len(s) > 0:
            if symbol in ("+", "-", "/", "*"):
                right = s.pop()
                left = s.pop()
                if symbol == "+":
                    plus = left + right
                elif symbol == "-":
                    plus = left - right
                elif symbol == "*":
                    plus = left * right
                elif symbol == "/":
                    plus = left / right
            else:
                raise Exception("unknown value: " + symbol)
        if plus is not None:
            s.append(plus)
    return s.pop()


HOST = "SERVER_IP_ADDRESS"
PORT = 9000
NUMBER_OF_SOCKETS = 1
BUFFER_SIZE = 1024
server_info = (HOST, PORT)
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
#we set the socket option to reuseable address of 1 so that we can quickly assign the socket after
#the previous socket (session of sorts) is terminated.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Server starting...")
#bind the socket we have assigned and listen for clients
sock.bind(server_info)
sock.listen(NUMBER_OF_SOCKETS)
#accept the client connection
connection, client_address = sock.accept()
cnt = 0
return_lines = list()
return_message = ""
data = ''
while True:
    print("Connection Address: " + str(client_address))
    while True:
        #read the data from the buffer between the client and server
        data = connection.recv(BUFFER_SIZE)
        #decode the data into a usable string format
        data = data.decode()
        #if the buffer is empty, we kill the loop and go read again
        if not data: break;
        #if the client notifies the server of an impending termination, we
        #give the client a couple of seconds to close its connection (gentler if client
        #goes first) and then we close the socket and connection
        if data == 'KILL':
            time.sleep(2.0)
            connection.close()
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            print("Connection and socket closed")
            break
        if data != None:
            print('message received:\n' + data)
            #break the lines up and compute the postfix operations
            #we then assign the values to a string for a return message and a list
            #structure (return_lines) if this were to be needed to properly address
            #individual results
            sent_lines = data.splitlines()
            for cnt in range(len(sent_lines)):
                return_lines.append(eval_postfix(sent_lines[cnt]))
                return_message = return_message + sent_lines[cnt] + " is equal to: " + str(eval_postfix(sent_lines[cnt]))
                return_message += '\n'
                ++cnt
            cnt = 0
            print(return_message)
            #send the results back to the client
            connection.send(return_message.encode())
            return_lines.clear()
            return_message = ""
    #the client has informed the server of its closing its connection, so we clear the data
    #variable and re-establish the socket and wait for any new connections to be made with appropriate clients
    data = ''
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_info)
    sock.listen(NUMBER_OF_SOCKETS)
    connection, client_address = sock.accept()
