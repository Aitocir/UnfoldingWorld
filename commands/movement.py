
def go(username, db, messenger, terms):
    player_state = db.get_component_for_entity('player_state', username)
    paths = db.get_component_for_entity('paths', player_state['location'])
    dest = ' '.join(terms[1:])
    if dest in paths['neighbors']:
        db.update_component_for_entity('player_state', {'location': dest}, username)
        resp = 'You {0} to {1}'.format(paths['neighbors'][dest], dest)
    else:
        resp = '"{0}" is not a valid destination from where you are currently standing. Try:{1}'.format(dest, '\n\t'.join(paths['neighbors']))    
    m = messenger.plain_text(resp, username)
    return [m]