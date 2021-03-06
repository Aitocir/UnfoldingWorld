
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

def search(username, db, messenger, command):
    if 'for' not in command:
        return [messenger.plain_text('For meaning? Happiness? What?!', username)]
    elif command['for'] == 'plants':
        return _search_for_plants(username, db, messenger)
    return [messenger.plain_text('Searching for "{0}" won\'t work here! (try "plants" instead)'.format(command['for']), username)]

def pick(username, db, messenger, command):
    if 'directobject' not in command:
        return [messenger.plain_text("Pick what? If you're gonna be greedy, at least be specific...", username)]
    elif 'from' not in command:
        return [messenger.plain_text("Pick from what? If you're gonna be greedy, at least be specific...", username)]
    amount = 1
    if 'directobject_num' in command:
        amount = command['directobject_num']
    if amount < 1:
        return [messenger.plain_text("Picking less than one of something doesn't really make sense, now does it?", username)]
    elif command['directobject'] not in set(['fruit']):
        return [messenger.plain_text('You can only "pick fruit from" plants for now, sorry :(', username)]
    item = command['directobject']
    plant_name = command['from']
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

def check(username, db, messenger, command):
    if 'directobject' not in command:
        return [messenger.plain_text("Mate!", username)]
    elif command['directobject'] == 'inventory':
        player_inv = db.get_component_for_entity('inventory', username)
        items = sorted(list(player_inv.keys()))
        lines = []
        for item in items:
            if item != 'entity' and player_inv[item] > 0:
                lines.append('{0} {1}'.format(player_inv[item], item))
        inv_desc = ', '.join(lines)
        if len(inv_desc) == 0:
            inv_desc = 'nothing'
        return [messenger.plain_text('Your inventory contains '+inv_desc, username)]
    else:
        return [messenger.plain_text("You can only check your inventory for now", username)]

def eat(username, db, messenger, command):
    if 'directobject' not in command:
        return [messenger.plain_text('Eat what?', username)]
    item = command['directobject']
    player_inv = db.get_component_for_entity('inventory', username)
    if item not in player_inv or player_inv[item] < 1:
        return [messenger.plain_text("You don't have any {0} to eat".format(item), username)]
    nutrition_label = db.get_component_for_entity('nutrition', item)
    if not nutrition_label:
        return [messenger.plain_text("{0} isn't edible, even if you really believe".format(item), username)]
    #  TODO: use info in nutrition label to modify player stats
    db.increment_property_of_component('player_state', username, 'hunger', -nutrition_label['energy'])
    db.increment_property_of_component('inventory', username, item, -1)
    return [messenger.plain_text("You eat 1 {0}".format(item), username)]