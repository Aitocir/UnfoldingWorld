#  OOC commands

def help(username, db, messenger, terms):
    return [messenger.plain_text('Available commands: check, eat, go, look, orient, pick, say, search, whisper', username)]