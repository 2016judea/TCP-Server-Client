import socket
import time

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


HOST = "192.168.1.107"
PORT = 9000
NUMBER_OF_SOCKETS = 1
BUFFER_SIZE = 1024
server_info = (HOST, PORT)
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Server starting...")
sock.bind(server_info)
sock.listen(NUMBER_OF_SOCKETS)
connection, client_address = sock.accept()
cnt = 0
return_lines = list()
return_message = ""
data = ''
while True:
    print("Connection Address: " + str(client_address))
    while True:
        data = connection.recv(BUFFER_SIZE)
        data = data.decode()
        if not data: break;
        if data == 'KILL':
            time.sleep(2.0)
            connection.close()
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            print("Connection and socket closed")
            break
        if data != None:
            print('message received:\n' + data)
            sent_lines = data.splitlines()
            for cnt in range(len(sent_lines)):
                return_lines.append(eval_postfix(sent_lines[cnt]))
                return_message = return_message + sent_lines[cnt] + " is equal to: " + str(eval_postfix(sent_lines[cnt]))
                return_message += '\n'
                ++cnt
            cnt = 0
            print(return_message)
            connection.send(return_message.encode())
            return_lines.clear()
            return_message = ""
    data = ''
    #print("Must wait at least 90 seconds before reusing same port and socket")
    #time.sleep(100)
    #print("Wait complete. Can now use socket and port")
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_info)
    sock.listen(NUMBER_OF_SOCKETS)
    connection, client_address = sock.accept()
