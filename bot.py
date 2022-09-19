import discord
import responses
import nltk
import json

from dotenv import load_dotenv
from neuralintents import GenericAssistant

assistant = GenericAssistant('intents.json', model_name="mangy")
assistant.train_model()
assistant.save_model()

async def send_message(message, user_message, is_private): # sends the message to the current channel or to the user
    try:
        response = responses.handle_response(user_message) # gets the response from responses.handle_response with user message
        await message.author.send(response) if is_private else await message.channel.send(response) # sends the response. if private, send to user, else send it to the channel
    except Exception as e: # prints error if it cant handle the message
        print(e)


def run_discord_bot():
    TOKEN = 'TOKEN' # get the token
    # Allows permissions to be granted for the bot to see the message
    intents = discord.Intents.default() 
    intents.message_content = True
    client = discord.Client(intents=intents) # The actual bot

    # Tells when bot is ready
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    # Responds to messages
    @client.event
    async def on_message(message):
        if message.author == client.user: # prevents endless loops (bot will read its own message fix)
            return

        # Gets the information the bot needs
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        split = user_message.split(' ')

        print(f"{username} said: '{user_message}' ({channel})") # Used for debugging

        if user_message[0] == '?': # user message looks like this [?, hello]
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, user_message, is_private=True) # Sends a private message
        else:
            await send_message(message, user_message, is_private=False)

        # Opens and loads intents.json
        with open('intents.json') as f:
            intents = json.load(f)

        patterns = [] # Empty list to store patterns keywords
        # Loops through patterns in json and puts them in list
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                patterns.append(pattern)

        res = [word for word in split if(word in patterns)] # List comprehension to check if word is in the list
        # If word is in patterns respond to user
        if bool(res) is True:
            if message.content.startswith("$MangyBot"): # If users message starts with '$MangyBot' reply to them using nerual intents
                response = assistant.request(message.content)
                await message.channel.send(f"{response} <@{message.author.id}>")

    client.run(TOKEN)