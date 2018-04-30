#  Unfolding World, the game!

import sys

from Pymug.gameserver import PymugServer

from commands.movement import *
from commands.system import *
from commands.talking import *

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
    server.set_game_thread_count(2)                 #  number of game threads to spawn to process player inputs
    server.set_connection_buffer(5)                 #  number of socket connections to queue up before refusing connections
    
    #
    #  add custom game logic
    server.register_player_command('go', go)
    server.register_player_command('say', say)
    server.register_player_command('whisper', whisper)
    
    #
    #  override system signals
    server.override_system_command('registered', init_player)
    server.override_system_command('logged-in', login_player)
    server.override_system_command('logged-out', logout_player)
    
    #
    server.init_db(['player_state', 'paths'])
    server.add_to_db('game', 'paths', {'entity': 'Origin Tree', 'neighbors': []})
    server.run()