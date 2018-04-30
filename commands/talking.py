
def say(username, db, messenger, terms):
    speech = ' '.join(terms[1:])
    location = db.get_component_for_entity('player_state', username)['location']
    others = db.get_matching_entities('player_state', {'location': location})
    messages = []
    for user in others:
        #  TODO: format more intelligently with 'you' for the speaker
        messages.append(messenger.plain_text('{0} says: "{1}"'.format(username, speech), user))
    return messages

def whisper(username, db, messenger, terms):
    dest = terms[1]
    if dest == username:
        return [messenger.plain_text('Whispering to yourself might make you look weird in front of NPCs which are yet to be added...', username)]
    speech = ' '.join(terms[2:])
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