
#  handle messages as Pymug server

import time
from thread import *

def socket_inbound(s, q, addr):
   overflowData = ''
   while 1:
      time.sleep(0.02)
      working = True
      packetSize = -1
      sizeSoFar = 0
      data = []
      if len(overflowData) > 0:
         data += overflowData
         sizeSoFar += len(overflowData)
         overflowData = ''
      while working:
         datum = s.recv(1024)
         if len(datum) == 0:
            s.close()
            if sizeSoFar > 0:
               q.put((addr, ''.join(data)))
            q.put((addr, ''))
            return
         data += datum
         sizeSoFar += len(datum)
         if sizeSoFar > 1 and packetSize == -1:
            soFar = ''.join(data)
            packetSize = (ord(soFar[0]) * 256) + ord(soFar[1])
         working = packetSize == -1 or sizeSoFar < (packetSize + 2)
      message = ''.join(data)
      if len(message) > 2:
         q.put(addr, (message[2:(packetSize+2)]))
         if len(message) > (packetSize + 2):
            overflowData = message[(packetSize+2):]

def socket_outbound(s, q, kill_cb):
   while 1:
      time.sleep(0.02)
      while not q.empty():
         m = q.get()
         mLen = len(m)
         byte0 = mLen // 256
         byte1 = mLen % 256
         message = chr(byte0) + chr(byte1) + m
         messLen = mLen + 2
         totalSent = 0
         while totalSent < messLen:
            sent = s.send(message[totalSent:])
            if sent == 0:
               s.close()
               kill_cb()
               return
            totalSent += sent

def deliver(q, debug):
    outboxes = {}
    while True:
        time.sleep(0.02)
        while not q.empty():
            task = q.get()
            if task[0] == 0:
                outboxes[task[1]] = task[2]
            elif task[0] == 1:
                if task[1] in outboxes:
                    outboxes[task[1]].put(task[2])
                elif debug:
                    print('unknown address: {0}'.format(task[1]))
            elif task[0] == 2:
                outboxes.pop(task[1])
        
class PostOffice:
    def __init__(self, port=29999, host='', backlog=5):
        self._s = socket.socket()
        self._s.bind((host, port))
        self._s.listen(backlog)
        self._oq = queue.Queue()
    def _coq(self, address):
        self._oq.put((2, address))
    def send(self, address, message):
        self._oq.put((0, address, message,))
    def run(self, inbox, debug=False):
        start_new_thread(deliver, (self._oq,debug,))
        while True:
            c, addr = s.accept()
            address = '::'.join([str(x) for x in addr])
            if debug:
                print('Got connection from: {0}'.format(address))
            outbox = queue.Queue()
            start_new_thread(socket_inbound,(c,inbox,addrStr,))
            start_new_thread(socket_outbound,(c,outbox,self._coq))
            self._oq.put((1, address, outbox))