import rethinkdb as r

class LoginDAO:
    def __init__(self, host='localhost', port=28015, db='login'):
        self._conn = r.connect(host=host, port=port, db=db)
    #
    #  save new user registration
    #  -> bool (saved successfully)
    def save_registration(self, username, password, email):
        result = r.table('registrations').insert({
            'username': username,
            'password': password,
            'email': email
        }).run(self._conn)
        return result['inserted'] == 1
    #
    #  check provided login against registration
    #  -> bool (username is valid for password)
    def check_login(self, username, password):
        result = r.table('registrations').get(username).run(self._conn)
        print(result)
        if result == None:
            return False  #  username not valid
        elif result['password'] != password:
            return False  #  wrong password
        else:
            return True   #  correct username and password