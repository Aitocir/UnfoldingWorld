
def _compile(words):
    if not len(words):
        return None, ''
    num = None
    if words[0].isdigit():
        num = int(words[0])
        words = words[1:]
    return num, ' '.join(words)

def _split_out_colons(terms):
    newterms = []
    for term in terms:
        if ':' in term:
            subterms = term.split(':')
            for sub in subterms:
                newterms.append(sub)
                newterms.append(':')
            newterms = newterms[:-1]
        else:
            newterms.append(term)
    return [term for term in newterms if len(term)]

#  parse user command text 
def user_command(text):
    terms = text.strip().split()
    terms = _split_out_colons(terms)
    cmd = {}
    if len(terms) == 0:
        return cmd
    cmd['verb'] = terms[0]
    mode = 'directobject'
    flags = ['with', 'by', 'from', 'for', 'to', ':']
    words = []
    for term in terms[1:]:
        if mode == ':':
            words.append(term)
        elif term in flags:
            num, cmd[mode] = _compile(words)
            if not len(cmd[mode]):
                cmd.pop(mode)
            if num:
                cmd[mode+'_num'] = num
            words = []
            mode = term
        else:
            words.append(term)
    if len(words):
        num, cmd[mode] = _compile(words)
        if num:
            cmd[mode+'_num'] = num
    return cmd