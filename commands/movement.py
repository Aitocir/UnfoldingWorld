#from .. import generators  #  generators.terrain import *

from generators.terrain import *

def _make_tile(px, py, db, dest):
    dest_tile, dest_plants = generate_tile(px, py)
    db.set_component_for_entity('tile', dest_tile, dest)
    for p in dest_plants:
        db.set_component_for_entity('plant', p, p['entity'])
    return dest_tile

def go(username, db, messenger, command):
    #
    #  validate input
    if 'directobject' not in command:
        return [messenger.plain_text('Go where?', username)]
    dir = command['directobject']
    if dir not in set(['north', 'south', 'east', 'west']):
        return [messenger.plain_text('Going {0} proves difficult... (Valid directions are north, south, east, and west)'.format(dir), username)]
    #
    #  gain bearing and determine destination
    player_state = db.get_component_for_entity('player_state', username)
    loc = player_state['location']
    px,py = [int(tmp) for tmp in loc.split(';')]
    if dir == 'north':
        py += 1
    if dir == 'south':
        py -= 1
    if dir == 'east':
        px += 1
    if dir == 'west':
        px -= 1
    dest = '{0};{1}'.format(px, py)
    dest_tile = db.get_component_for_entity('tile', dest)
    #
    #  execute
    if not dest_tile:
        _make_tile(px, py, db, dest)
    db.update_component_for_entity('player_state', {'location': dest}, username)
    resp = 'You walk {0}'.format(dir)
    m = messenger.plain_text(resp, username)
    return [m]

def look(username, db, messenger, command):
    #
    #  validate input
    if 'directobject' not in command:
        return [messenger.plain_text('Look where?', username)]
    target = command['directobject']
    if target not in set(['north', 'south', 'east', 'west', 'around']):
        return [messenger.plain_text('Looking {0} proves difficult... (Valid options are north, south, east, west, and around)'.format(target), username)]
    #
    #  do the looking
    player_state = db.get_component_for_entity('player_state', username)
    loc = player_state['location']
    px,py = [int(tmp) for tmp in loc.split(';')]
    if target == 'north':
        py += 1
    if target == 'south':
        py -= 1
    if target == 'east':
        px += 1
    if target == 'west':
        px -= 1
    dest = '{0};{1}'.format(px, py)
    dest_tile = db.get_component_for_entity('tile', dest)
    #
    #  execute
    if not dest_tile:
        dest_tile = _make_tile(px, py, db, dest)
    resp = 'You look {0}, and see {1}'.format(target, dest_tile['biome'])
    m = messenger.plain_text(resp, username)
    return [m]

def orient(username, db, messenger, command):
    #  no parameters for this command, so anything is valid
    player_state = db.get_component_for_entity('player_state', username)
    loc = player_state['location']
    px,py = [int(tmp) for tmp in loc.split(';')]
    ns = 'north' if py>0 else 'south'
    ew = 'east' if px>0 else 'west'
    ns_text = '' if py==0 else '{0} tile{2} {1}'.format(abs(py), ns, 's' if abs(py)>1 else '')
    ew_text = '' if px==0 else '{0} tile{2} {1}'.format(abs(px), ew, 's' if abs(px)>1 else '')
    joiner = ' and ' if len(ns_text) and len(ew_text) else ''
    full_desc = ns_text + joiner + ew_text
    if len(full_desc):
        full_desc += ' of'
    else:
        full_desc = 'at'
    return [messenger.plain_text("You are {0} The Origin".format(full_desc), username)]