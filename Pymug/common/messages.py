
#
#  Public message preparers
#

def plain_text(text, dest=None):
    return (0, 0, dest, text)

#
#  Public message analyzers
#

def dest(m):
    return m[2]

def payload(m):
    return m[3]

def is_plain_text(m):
    return m[1] == 0

#
#  Private message network formatting
#

def _unpack(package):
    if package[0] == 0:   #  plain text
        content = str(package[1:], encoding='utf-8')
    return content

def _pack(m):
    stuff = m[3]
    dest = m[2]
    type = m[1]
    if type == 0:
        header = bytes([0])
        body = bytes(stuff, encoding='utf-8')
    if dest:
        return dest, header+body
    return header+body