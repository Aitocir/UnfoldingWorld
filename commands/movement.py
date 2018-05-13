#from .. import generators  #  generators.terrain import *

from generators.terrain import *

def go(username, db, messenger, terms):
    #
    #  validate input
    if len(terms) < 2:
        return [messenger.plain_text('Go where?', username)]
    if terms[1] not in set(['north', 'south', 'east', 'west']):
        return [messenger.plain_text('Going {0} proves difficult... (Valid directions are north, south, east, and west)'.format(terms[1]), username)]
    #
    #  gain bearing and determine destination
    player_state = db.get_component_for_entity('player_state', username)
    loc = player_state['location']
    px,py = [int(tmp) for tmp in loc.split(';')]
    if terms[1] == 'north':
        py += 1
    if terms[1] == 'south':
        py -= 1
    if terms[1] == 'east':
        px += 1
    if terms[1] == 'west':
        px -= 1
    dest = '{0};{1}'.format(px, py)
    dest_tile = db.get_component_for_entity('tile', dest)
    #
    #  execute
    if not dest_tile:
        dest_tile, dest_plants = generate_tile(px, py)
        db.set_component_for_entity('tile', dest_tile, dest)
        for p in dest_plants:
            db.set_component_for_entity('plant', p, p['entity'])
    db.update_component_for_entity('player_state', {'location': dest}, username)
    resp = 'You walk {0}'.format(terms[1])
    m = messenger.plain_text(resp, username)
    return [m]
    