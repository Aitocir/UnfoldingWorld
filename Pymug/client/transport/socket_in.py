import time

def _packet(data):
    return bytes(data)

def _close():
    return None

def recv_socket(s, q, lenbytes=2):
    overflowData = bytearray()
    while True:
        time.sleep(0.02)
        working = True
        packetSize = -1
        data = bytearray()
        data += overflowData
        overflowData = bytearray()
        while working:
            datum = s.recv(1024)
            if len(datum) == 0:
                s.close()
                q.put(_close())
                print('closing recv_socket')
                return
            data += datum
            if len(data) >= lenbytes and packetSize == -1:
                packetSize = int.from_bytes(data[:lenbytes], 'big')
                data = data[lenbytes:]
            working = packetSize == -1 or len(data) < packetSize
        message = data[:packetSize]
        q.put(_packet(message))
        overflowData = data[packetSize:]