
def grow_plants(db, messenger, object):
    #
    #  grow plant
    db.increment_property_of_component('plant', object['entity'], 'growth', object['growth_rate'])
    return []

def ripen_fruit(db, messenger, object):
    db.increment_property_of_component('plant', object['entity'], 'fruit_growth', object['fruit_growth_rate'])
    return []