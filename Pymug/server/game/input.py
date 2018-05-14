from .parse import user_command

#  processes typed commands
def process_typed_input(q, q_output, player_commands, system_commands, db, messenger):
    while True:
        task = q.get()
        #
        #  user input
        if task[0] == 0:
            if not messenger.is_plain_text(task):
                raise ValueError('Non-plain-text message passed to typed input processor')
            username = messenger.dest(task)
            command = user_command(messenger.payload(task))
            print(command)
            if not command:
                continue
            if command['verb'] in player_commands:
                output_messages = player_commands[command['verb']](username, db, messenger, command)
                for m in output_messages:
                    q_output.put(m)
            else:
                q_output.put(messenger.plain_text('Unknown command: "{0}"'.format(command['verb']), username))
        #
        #  automated input
        elif task[0] == 1:
            if task[2] in system_commands:
                output_messages = system_commands[task[2]](task[1], db, messenger)
                for m in output_messages:
                    q_output.put(m)