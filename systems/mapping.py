import opensimplex as os

"""
Included for demonstrating intent, and possibly future use. In this case, we cannto keep the generator in memory,
so succeeding coordinates must be generated based on previous values.

def _coord_spiral(cx, cy, bx=None, by=None):
    x = 0
    y = 0
    o = 1
    f = 1
    if bx==None or by==None:
        ready = True
    elif bx==cx and by==cy:
        ready = True
    else:
        ready = False
    while True:
        for xoffset in range(o):
            x += f * xoffset
            if ready:
                yield (x, y)
            else:
                ready = bx==x and by==y
        for yoffset in range(o):
            y += f * yoffset
            if ready:
                yield (x, y)
            else:
                ready = bx==x and by==y
        o += 1
        f *= -1
"""

def _next_spiral_coord(x, y):
    #
    #  init case
    if x==0 and y==0:
        return (1,0)
    #
    #  diagonal axes cases
    if x>0 and x==y:
        return (x-1, y)
    if x<0 and -x==y:
        return (x, y-1)
    if x<0 and x==y:
        return (x+1, y)
    if x>0 and -x==y:
        return (x+1, y)  #  special case! doesn't change from right to up until next square
    #
    #  straight edge cases
    if x > 0 and abs(x) > abs(y):
        return (x, y+1)
    if y > 0 and abs(x) < abs(y):
        return (x-1, y)
    if x < 0 and abs(x) > abs(y):
        return (x, y-1)
    if y < 0 and abs(x) < abs(y):
        return (x+1, y)
    raise ValueError('somehow I missed a case! :-O')

def generate_world_location(db, messenger):
    #
    #  find place (in case of partially generated world)
    bookmark = db.get_component_for_entity('tile', 'generation_bookmark')
    if not bookmark:
        x = 0
        y = 0
    else:
        x = bookmark['x']
        y = bookmark['y']
    new_coord = _next_spiral_coord(x, y)
    print('{0}:{1} -> {2}'.format(x, y, new_coord))
    #
    #  create new tile
    tile_name = '{0};{1}'.format(*new_coord)
    #  TODO: procedurally generate unique plant types based on terrain ... also have some different terrain
    db.set_component_for_entity('tile', {'growth_rate': 4, 'growth': 100, 'max_quantity': 25, 'plant': 'huckleberry bush', 'resource': 'huckleberries'}, tile_name)
    db.set_component_for_entity('tile', {'x': new_coord[0], 'y': new_coord[1]}, 'generation_bookmark')
    #
    #  announce to nearby players
    nearby_users = []
    nearby_users.extend(db.get_matching_entities('player_state', {'location': '{0};{1}'.format(new_coord[0]-1, new_coord[1])}))
    nearby_users.extend(db.get_matching_entities('player_state', {'location': '{0};{1}'.format(new_coord[0], new_coord[1]-1)}))
    nearby_users.extend(db.get_matching_entities('player_state', {'location': '{0};{1}'.format(new_coord[0]+1, new_coord[1])}))
    nearby_users.extend(db.get_matching_entities('player_state', {'location': '{0};{1}'.format(new_coord[0], new_coord[1]+1)}))
    messages = [messenger.plain_text('Nearby mist has cleared!', user) for user in nearby_users]
    return messages
    
    