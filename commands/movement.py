
_loc_types = {
    'Camp': {}, 
    'Road': {}, 
    'Valley': {}, 
    'Meadow': {}, 
    'Field': {}
    }
    
_loc_desc = {
    'Golden': {},
    'Gilded': {},
    'Haunted': {},
}

def _generate_locname(depth):
    pass

def _generate_location(depth, origin):
    pass
    """
    loc = {}
    loc['depth'] = depth
    paths = [origin]
    """

def _ensure_location(db, origin, loc, depth):
    pass
    """
    loc = db.get_component_for_entity('paths', player_state['location'])
    if loc==None:
        loc = _generate_location(depth, origin)
        db.set_component_for_entity('paths', loc, loc['entity'])
    """

def go(username, db, messenger, terms):
    player_state = db.get_component_for_entity('player_state', username)
    loc = db.get_component_for_entity('paths', player_state['location'])
    dest = ' '.join(terms[1:])
    if dest in loc['neighbors']:
        _ensure_location(db, player_state['location'], dest, loc['depth']+1)
        db.update_component_for_entity('player_state', {'location': dest}, username)
        resp = 'You {0} to {1}'.format(loc['neighbors'][dest], dest)
    else:
        resp = '"{0}" is not a valid destination from where you are currently standing. Try:{1}'.format(dest, '\n\t'.join(loc['neighbors']))    
    m = messenger.plain_text(resp, username)
    return [m]
    