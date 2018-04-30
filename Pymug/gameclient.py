#  main client file

import socket
import ssl
import sys
import queue
import time
from _thread import start_new_thread

from client.transport.socket_in import recv_socket
from client.transport.socket_out import send_socket
from client.transport import courier

import common.messages as messenger

#  TODO: make this enterable (have a non-connected mode for client with connect, quit, settings commands)
host = 'localhost'
port = 29999

sock = socket.socket()
s = ssl.wrap_socket(sock, server_side=False, ssl_version=ssl.PROTOCOL_TLSv1_2)
s.connect((host, port))

qrecv = queue.Queue()
qsend = queue.Queue()
start_new_thread(recv_socket, (s, qrecv,))
start_new_thread(send_socket, (s, qsend,))

#  TODO: real UI with different input and output text boxes
start_new_thread(courier.print_responses, (qrecv,messenger,))

while True:
    
    line = input().strip()
    if line == 'exit':
        break
    
    message = messenger._pack(messenger.plain_text(line))
    qsend.put(message)
    
    
s.close()
