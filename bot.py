import os
import sys, subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "-U","python-dotenv", "discord-py-interactions"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "-U","wikipedia"])

import interactions
from dotenv import load_dotenv
import wikipedia as wp
load_dotenv()

wp.set_lang("pt")

TOKEN = os.getenv("TOKEN")
PREFIXO_NORMAL = os.getenv("PREFIXO_NORMAL")
PREFIXO_RPG = os.getenv("PREFIXO_RPG")
GUILD_ID = int(os.getenv("GUILD_ID"))

comprimento = len(PREFIXO_NORMAL)
clear_prefixed_lenth = len((PREFIXO_NORMAL + "clear"))

client = interactions.Client(TOKEN, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT)

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
		
		if message.content[comprimento: clear_prefixed_lenth] == "clear":
			value = int(message.content[(clear_prefixed_lenth + 1): ])
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
	# Comandos com o prefixo de rpg ( ? )

#Slash Commands
@client.command(
    name="ping",
    description="Devolve a latência da api do bot",
    scope=GUILD_ID
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send(f'O bot está com uma latência de {(round(client.latency, 3)*1000)} ms')

client.start()


