import os, sys, subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "-U","python-dotenv", "discord-py-interactions"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "-U","wikipedia"])

import interactions
from dotenv import load_dotenv
import wikipedia as wp

load_dotenv()

wp.set_lang("pt")

TOKEN = (os.getenv("TOKEN1") + os.getenv("TOKEN2"))
PREFIXO_STAFF = ":"
PREFIXO_RPG = "?"
GUILD_ID = int(906962728533516319)

comprimento = len(PREFIXO_STAFF)

client = interactions.Client(TOKEN, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT)

#on ready
@client.event
async def on_ready():
    print(f'{client.me.name} has connected to Discord!')


@client.event
async def on_message_create(message):
	# Comandos com o prefixo geral ( : )
	if message.content[0:comprimento] == PREFIXO_STAFF:
		if message.content[comprimento: ] == "ping":
			channel = await message.get_channel()
			await message.delete()
			await channel.send(f'O bot está com uma latência de {(round(client.latency, 3)*1000)} ms')
		
		#if message.content[comprimento:(comprimento + len("clear"))] == "clear":
		#	value = int(message.content[((comprimento + len("clear")) + 1): ])
		#	channel = await message.get_channel()
		#	await channel.purge(limit=(value + 1))
		#	await channel.send(f'As mensagens foram limpas do {message.channel.name}')

		for n in ["realitas", "wikipedia"]:
			if (message.content[comprimento:(comprimento + len(n))] == n):
				channel = await message.get_channel()
				content = message.content[(comprimento + len(n) + 1 ) : ]
				await channel.send(wp.summary(str(content), sentences=1))
				await message.delete()



# Comandos com o prefixo de rpg ( ? )

#Slash Commands
@client.command(
	name="ping",
	description="Devolve a latência da api do bot",
	scope=GUILD_ID)
async def ping(ctx: interactions.CommandContext):
	await ctx.send(f'O bot está com uma latência de {round(client.latency, 3)} ms')

for n in ["realitas", "wikipedia"]:
	@client.command(
		name=n,
		description="Pesquisa na Wikipédia sobre o assunto",
		scope=GUILD_ID
	)
	@interactions.option("Assunto")
	async def wiki(ctx: interactions.CommandContext, assunto: str):
		await ctx.send(wp.summary(str(assunto), sentences=1))








client.start()


