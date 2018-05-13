
def pack_text(text):
    return bytes(text, encoding='utf-8')

def process_responses(in_q, out_q, messenger):
    while True:
        content = messenger._unpack(in_q.get())
        out_q.put(content)

def process_requests(in_q, out_q, messenger):
    while True:
        content = in_q.get()
        payload = messenger._pack(messenger.plain_text(content))
        out_q.put(payload)