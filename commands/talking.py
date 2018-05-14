
def say(username, db, messenger, command):
    if ':' not in command:
        return [messenger.plain_text("say: <stuff to say out loud>", username)]
    speech = command[':']
    location = db.get_component_for_entity('player_state', username)['location']
    others = db.get_matching_entities('player_state', {'location': location})
    messages = []
    for user in others:
        #  TODO: format more intelligently with 'you' for the speaker
        messages.append(messenger.plain_text('{0} says: "{1}"'.format(username, speech), user))
    return messages

def whisper(username, db, messenger, command):
    if 'to' not in command or command['to'] == username:
        return [messenger.plain_text('Whispering to yourself might make you look weird in front of NPCs which are yet to be added...', username)]
    dest = command['to']
    if ':' not in command:
        return [messenger.plain_text('whisper to <username>: <stuff to whisper>', username)]
    speech = command[':']
    location_src = db.get_component_for_entity('player_state', username)['location']
    dst_state = db.get_component_for_entity('player_state', dest)
    location_dst = None if dst_state==None else dst_state['location']
    messages = []
    if location_dst == None or location_dst!=location_src or dst_state['status']=='offline':
        messages.append(messenger.plain_text('"{0}" isn\'t around to hear you whispering.'.format(dest), username))
    elif dst_state['status']=='active':
        messages.append(messenger.plain_text('{0} whispers to you: "{1}"'.format(username, speech), dest))
        messages.append(messenger.plain_text('You whisper to {0}: "{1}"'.format(dest, speech), username))
    elif dst_state['status']=='afk':
        messages.append(messenger.plain_text('{0} whispers to you: "{1}"'.format(username, speech), dest))
        messages.append(messenger.plain_text('You whisper to {0}: "{1}"'.format(dest, speech), username))
        messages.append(messenger.plain_text('Warning: {0} is currently AFK'.format(dest), username))
    return messages