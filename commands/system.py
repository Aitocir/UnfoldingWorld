import time

def init_player(username, db, messenger):
    db.set_component_for_entity('player_state', {'last_login':0, 'location':'Origin Tree', 'status':'offline'}, username)
    return []

def login_player(username, db, messenger):
    status = db.get_component_for_entity('player_state', username)
    last_login = status['last_login']
    db.update_component_for_entity('player_state', {'status': 'active', 'last_login': int(time.time())}, username)
    return [messenger.plain_text("Welcome {1}to Unfolding World, {0}!\n\n".format(username, '' if last_login!=0 else 'back '), username)]

def logout_player(username, db, messenger):
    db.update_component_for_entity('player_state', {'status': 'offline'}, username)
    return []