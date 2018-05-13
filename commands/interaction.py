
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

def pick(username, db, messenger, terms):
    if len(terms) < 2:
        return [messenger.plain_text("Pick what? If you're gonna be greedy, at least be specific...", username)]
    elif len(terms) < 4:
        return [messenger.plain_text("Pick from what? If you're gonna be greedy, at least be specific...", username)]
    amount = 1
    offset = 0
    if terms[1].isdigit():
        amount = int(terms[1])
        offset = 1
    if amount < 1:
        return [messenger.plain_text("Picking less than one of something doesn't really make sense, now does it?", username)]
    elif terms[2+offset] != 'from' or terms[1+offset] not in set(['fruit']):
        return [messenger.plain_text('You can only "pick fruit from" plants for now, sorry :(', username)]
    item = terms[1+offset]
    plant_name = ' '.join(terms[3+offset:])
    player_state = db.get_component_for_entity('player_state', username)
    plant_entity = player_state['location']+';'+plant_name
    plant = db.get_component_for_entity('plant', plant_entity)
    if plant == None:
        return [messenger.plain_text("There isn't a {0} nearby to pick {1} from.".format(plant_name, item), username)]
    elif item not in plant:
        return [messenger.plain_text("There aren't any {0} on the {1}.".format(item, plant_name), username)]
    if plant[item+'_growth'] < (100 / plant[item+'_count']) * amount:
        return [messenger.plain_text("There aren't enough {0} on the {1} to pick that many!".format(item, plant_name), username)]
    db.increment_property_of_component('plant', plant_entity, item+'_growth', (-100 / plant[item+'_count']) * amount)
    db.increment_property_of_component('inventory', username, plant[item], amount)
    return [messenger.plain_text("You pick {0} {1} off the nearby {2}".format(amount, plant[item], plant_name), username)]
    