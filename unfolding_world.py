#  Unfolding World, the game!

import sys

from Pymug.gameserver import PymugServer

from commands.movement import *
from commands.system import *
from commands.talking import *
from commands.interaction import *

from systems.mapping import *
from systems.growing import *

if __name__ == '__main__':
    
    if len(sys.argv)<3:
        print('must provide public cert and key files on command line to run this example')
        exit()
    
    #
    #  configure server
    server = PymugServer(sys.argv[1], sys.argv[2])  #  init server with TLS cert and key
    server.set_server_host('')                      #  change server host (empty string means all available host names)
    server.set_server_port(29999)                   #  change server port used for hosting
    server.set_db_host('localhost')                 #  change hostname used to connect to database
    server.set_db_port(28015)                       #  change port used to connect to database
    server.set_game_thread_count(5)                 #  number of game threads to spawn to process player inputs
    server.set_connection_buffer(5)                 #  number of socket connections to queue up before refusing connections
    
    #
    #  add custom game logic
    server.register_player_command('check', check)
    server.register_player_command('eat', eat)
    server.register_player_command('go', go)
    server.register_player_command('look', look)
    server.register_player_command('orient', orient)
    server.register_player_command('pick', pick)
    server.register_player_command('say', say)
    server.register_player_command('search', search)
    server.register_player_command('whisper', whisper)
    
    #
    #  override system signals
    server.override_system_command('registered', init_player)
    server.override_system_command('logged-in', login_player)
    server.override_system_command('logged-out', logout_player)
    
    #
    #  define ECS systems
    #server.define_ecs_timer_system('map_reveal', generate_world_location, 10)
    server.define_ecs_clock_system('plant_growing', 'plant', grow_plants, 
        [('growth', '<', 100)], 60, 10)
    server.define_ecs_clock_system('fruit_ripening', 'plant', ripen_fruit, 
        [('fruit_growth', '<', 100)], 60, 10)
    
    #
    server.init_db_with_ecs_components(['player_state', 'tile', 'plant', 'inventory', 'nutrition'])
    server.add_to_db('game', 'tile', {'entity': '0;0', 'plants': [], 'elevation': 0.5, 'moisture': 0.5, 'temperature': 0.5, 'biome': 'THE ORIGIN'})
    server.add_to_db('game', 'nutrition', {'entity': 'apples'})         #  TODO: add actual nutrition info
    server.add_to_db('game', 'nutrition', {'entity': 'fire berries'})   #  TODO: add actual nutrition info
    server.run()