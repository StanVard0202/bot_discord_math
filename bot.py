import os, sys, subprocess
from commands import *

subprocess.check_call([sys.executable, "-m", "pip", "install", "-U","python-dotenv", "discord-py-interactions"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "-U","wikipedia"])

import interactions
from dotenv import load_dotenv
import wikipedia as wp

load_dotenv()

wp.set_lang("pt")

TOKEN = (os.getenv("TOKEN1") + os.getenv("TOKEN2"))
PREFIXO_NORMAL = ":"
PREFIXO_RPG = "?"
GUILD_ID = int(906962728533516319)

comprimento = len(PREFIXO_NORMAL)

client = interactions.Client(TOKEN, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT)

commands(interactions.CommandContext, client, GUILD_ID)

#on ready
@client.event
async def on_ready():
    print(f'{client.me.name} has connected to Discord!')


@client.event
async def on_message_create(message):
	# Comandos com o prefixo geral ( : )
	if message.content[0:comprimento] == PREFIXO_NORMAL:
		if message.content[comprimento: ] == "ping":
			channel = await message.get_channel()
			await message.delete()
			await channel.send(f'O bot está com uma latência de {(round(client.latency, 3)*1000)} ms')
		
		if message.content[comprimento: (len((PREFIXO_NORMAL + "clear")))] == "clear":
			value = int(message.content[(len((PREFIXO_NORMAL + "clear")) + 1): ])
			channel = await message.get_channel()
			await message.channel.purge(limit=(value + 1))
			await channel.send(f'As mensagens foram limpas do {message.channel.name}')

		if message.content[comprimento: ] == "hello":
			channel = await message.get_channel()
			await channel.send("hey dirtbag")
			await message.delete()
		
		if (message.content[comprimento:(comprimento + len("realitas"))] == "realitas"):
			channel = await message.get_channel()
			content = message.content[(comprimento + len("realitas") + 1 ) : ]
			await channel.send(wp.summary(str(content), sentences=1))
			await message.delete()

		if (message.content[comprimento:(comprimento + len("wikipedia"))] == "wikipedia"):
			channel = await message.get_channel()
			content = message.content[(comprimento + len("wikipedia") + 1 ) : ]
			await channel.send(wp.summary(str(content), sentences=1))
			await message.delete()



	# Comandos com o prefixo de rpg ( ? )

#Slash Commands


client.start()


