import time

def send_socket(s, q, lenbytes=2):
    while True:
        time.sleep(0.02)
        while not q.empty():
            m = q.get()
            print('sending packet: {0}'.format(m))
            mLen = len(m).to_bytes(lenbytes, 'big')
            message = mLen + m
            messLen = len(message)
            totalSent = 0
            while totalSent < messLen:
                sent = s.send(message[totalSent:])
                if sent == 0:
                    s.close()
                    print('closing send_socket')
                    return
                totalSent += sent
