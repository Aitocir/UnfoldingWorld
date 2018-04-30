#  Example pymug server (list registered and online players)

import sys

from Pymug.gameserver import PymugServer

def welcome_player(username, db, messenger):
    db.set_component_for_entity('status', {'online': True}, username)
    return [messenger.plain_text("Welcome to the Ex00-basic-server, {0}!\n\nWe've missed you :)".format(username), username)]

def goodbye_player(username, db, messenger):
    db.set_component_for_entity('status', {'online': False}, username)
    return []

def list_players(username, db, messenger, terms):
    if len(terms) != 2:
        return [messenger.plain_text('Usage: "list <online | all>"', username)] 
    elif terms[1] == 'online':
        online_users = db.get_matching_entities('status', {'online': True})
        userlist = '\n'.join(online_users)
        return [messenger.plain_text('The following users are online:\n\n{0}'.format(userlist), username)]
    elif terms[1] == 'all':
        online_users = db.get_all_entities('status')
        userlist = '\n'.join(online_users)
        return [messenger.plain_text('The following users are registered with this server:\n\n{0}'.format(userlist), username)]
    else:
        return [messenger.plain_text('Usage: "list <online | all>"', username)]

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
    server.register_player_command('list', list_players)
    
    #
    #  override system signals
    server.override_system_command('registered', goodbye_player)
    server.override_system_command('logged-in', welcome_player)
    server.override_system_command('logged-out', goodbye_player)
    
    #
    server.init_db(['status'])
    server.run()