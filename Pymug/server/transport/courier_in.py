#  object used to process incoming socket traffic

from _thread import start_new_thread

class CourierInbound:
    def __init__(self, q_inbound, q_courier_out, q_game, userdb, messenger):
        self._q = q_inbound
        self._qout = q_courier_out
        self._qgame = q_game
        self._users = {}
        self._db = userdb
        self._m = messenger
    def _build_client_mapping(self, username, cid):
        return (2, username, cid)
    def _build_system_signal(self, username, type):
        return (1, username, type)
    def _parse_anon_payload(self, payload):
        form = payload.split()
        if len(form) == 3 and form[0] == 'login':
            return {'type':form[0], 'username':form[1], 'password':form[2]}
        elif len(form) == 4 and form[0] == 'register':
            return {'type':form[0], 'username':form[1], 'password':form[2], 'email':form[3]}
        else:
            return None
    def _validate_registration(self, username, password, email):
        #  TODO: actual validation of any kind
        uvalid = True
        pvalid = True
        evalid = '@' in email
        return uvalid and pvalid and evalid
    def _handle_anon_traffic(self, cid, payload):
        form = self._parse_anon_payload(payload)
        if not form:
            self._qout.put(self._m.plain_text('login <username> <password>\nregister <username> <password> <email>', cid))
        elif form['type'] == 'login':
            if self._db.check_login(form['username'], form['password']):
                self._users[cid] = form['username']
                self._qout.put(self._build_client_mapping(form['username'], cid))
                self._qgame.put(self._build_system_signal(form['username'], 'logged-in'))
            else:
                self._qout.put(self._m.plain_text('Wrong username or password', cid))
        elif form['type'] == 'register':
            if self._validate_registration(form['username'], form['password'], form['email']):
                if self._db.save_registration(form['username'], form['password'], form['email']):
                    self._qgame.put(self._build_system_signal(form['username'], 'registered'))
                    #  TODO: remove this once the system signal generates this message
                    self._qout.put(self._m.plain_text('Successfully registered {0}! Now try logging in'.format(form['username']), cid))
                else:
                    self._qout.put(self._m.plain_text('Username {0} already exists; try logging in.'.format(form['username']), cid))
            else:
                self._qout.put(self._m.plain_text('bad values provided for registration form (is your email valid?)', cid))
    def _loop(self):
        while True:
            task = self._q.get()
            print(task)
            if task[0] == 0:    #  traffic from a socket
                cid = task[1]
                payload = self._m._unpack(task[2])
                #  For now, server only accepts plain text messages from client
                if not isinstance(payload, str):
                    #  TODO: send client error message indicating incompatible payload
                    continue
                #
                #  not logged in
                if not self._users[cid]:
                    self._handle_anon_traffic(cid, payload)
                #
                #  logged in
                else:
                    self._qgame.put(self._m.plain_text(payload, self._users[cid]))
            elif task[0] == 1:  #  new address
                cid = task[1]
                self._users[cid] = None
            elif task[0] == -1: #  closed socket
                self._qgame.put(self._build_system_signal(self._users.pop(task[1]), 'logged-out'))
                self._qout.put(task)
                print('socket closed: {0}'.format(task[1]))
    def run(self):
        start_new_thread(self._loop, tuple())