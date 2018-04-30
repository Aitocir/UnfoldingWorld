import rethinkdb as r
import sys

from generation.locations import *

if __name__ == '__main__':
    #
    #  parameters
    db_host = sys.argv[1]
    db_port = sys.argv[2]
    db_exists = len(sys.argv[3]) > 3
    
    #
    #  init database 
    #  (don't forget to have this running already!)
    conn = r.connect(host=db_host, port=db_port)
    
    if db_exists:
        r.db_drop('login').run(conn)
        r.db_drop('game').run(conn)
    
    r.db_create('login').run(conn)
    r.db('login').table_create('registrations', primary_key='username').run(conn)
    
    r.db_create('game').run(conn)
    r.db('game').table_create('location', primary_key='entity').run(conn)
    r.db('game').table_create('inventory', primary_key='entity').run(conn)
    r.db('game').table_create('trade-offers', primary_key='entity').run(conn)
    r.db('game').table_create('paths', primary_key='entity').run(conn)
    
    locations = generate_world_locations()
    for location in locations:
        r.db('game').table('paths').insert({
            'place': location,
            'visible_destinations': locations[location]['visible_neighbors'],
            'hidden_destinations': []
        })
    
    conn.close()