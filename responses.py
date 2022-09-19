import random


def handle_response(message) -> str: # returns a response of your choice
    p_message = message.lower() # lower cases the message
    if p_message == 'hello':
        return 'Hey there!'

    if p_message == 'roll':
        return str(random.randint(1, 6))
    
    if p_message == '!help':
        return "`This is a help message that you can modify.`" # backwards ticks used to identify a code section