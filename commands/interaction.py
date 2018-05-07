
def _search_for_plants(username, db, messenger):
    player = db.get_component_for_entity('player_state', username)
    location = player['location']
    tile = db.get_component_for_entity('tile', location)
    if 'plant' not in tile or tile['plant'] != 'none':
        desc = 'You spy a {0} nearby.'.format(tile['plant'])
    else:
        desc = "You don't see any plants of value in the area."
    return [messenger.plain_text(desc, username)]

def search(username, db, messenger, terms):
    if len(terms) < 2:
        return [messenger.plain_text('For meaning? Happiness? What?!', username)]
    elif terms[1] == 'plants':
        return _search_for_plants(username, db, messenger)
    return [messenger.plain_text('Searching for "{0}" won\'t work here! (try "plants" instead)'.format(terms[1]), username)]
