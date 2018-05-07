
def grow_plants(db, messenger, object):
    #
    #  grow plant
    object['growth'] += object['growth_rate']
    db.update_component_for_entity('tile', object, object['entity'])
    return []