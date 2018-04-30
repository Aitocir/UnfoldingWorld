import random

def _generate_roads():
    

def generate_world_locations():
    #  TODO: generate these procedurally
    locations = {}
    locations['Ughdale'] = {
        'visible_neighbors': ['bandit camp'],
        }
    locations['bandit camp'] = {
        'visible_neighbors': ['Ughdale', 'Capitol City'], 
        }
    locations['Capitol City'] = {
        'visible_neighbors': ['bandit camp'], 
        }
    return locations