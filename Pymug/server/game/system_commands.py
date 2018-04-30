#  system command definitions
#  all functions should return lists of (username, message) tuples

def _init(username, db, messenger):
    #  This event is triggered when a player is first registered
    #  convenient signal for initializing database records for brand new players
    return []

def _login(username, db, messenger):
    #  This event is triggered when a player logs in
    #  convenient signal for sending welcome messages, server announcements, etc.
    return [messenger.plain_text('Welcome to this generic pymug server, {0}!'.format(username), username)]

def _logout(username, db, messenger):
    #  This event is triggered when a player logs out (gracefully or not)
    #  convenient signal for marking player as offline
    return []

def system_cmds():
    return {
        'registered': _init,
        'logged-in': _login,
        'logged-out': _logout
    }