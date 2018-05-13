
def _phrase_list(items):
    joiner = ', a '
    header = 'a '
    final_joiner = ', and a '
    if len(items) == 1:
        return header+items[0]
    most_of_list = header+joiner.join(items[:-1])
    full_list = most_of_list+final_joiner+items[-1]
    return full_list

def _search_for_plants(username, db, messenger):
    player = db.get_component_for_entity('player_state', username)
    location = player['location']
    tile = db.get_component_for_entity('tile', location)
    plant_entities = tile['plants']
    if len(plant_entities):
        desc = 'You spy {0} nearby.'.format(_phrase_list(plant_entities))
    else:
        desc = "You don't see any plants of value in the area."
    return [messenger.plain_text(desc, username)]

def search(username, db, messenger, terms):
    if len(terms) < 2:
        return [messenger.plain_text('For meaning? Happiness? What?!', username)]
    elif terms[1] == 'plants':
        return _search_for_plants(username, db, messenger)
    return [messenger.plain_text('Searching for "{0}" won\'t work here! (try "plants" instead)'.format(terms[1]), username)]
