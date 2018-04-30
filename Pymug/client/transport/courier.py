
def pack_text(text):
    return bytes(text, encoding='utf-8')

def print_responses(q, messenger):
    while True:
        content = messenger._unpack(q.get())
        print(content)