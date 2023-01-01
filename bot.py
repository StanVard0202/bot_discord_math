import os, sys, subprocess
from energia import *

state = False

packages = ["python-dotenv", "discord-py-interactions", "wikipedia"]
for i in packages:
	if True:
		subprocess.check_call([sys.executable, "-m", "pip", "install", "-U",str(i)])
	else:
		print("skipped")



import interactions
from dotenv import load_dotenv
import wikipedia as wp
from random import randint

load_dotenv()

wp.set_lang("pt")

TOKEN = (os.getenv("TOKEN1") + os.getenv("TOKEN2"))
PREFIXO_STAFF = ":"
PREFIXO_RPG = "?"
GUILD_ID = int(906962728533516319)

comprimento = len(PREFIXO_RPG)

client = interactions.Client(TOKEN, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT)

#on ready
@client.event
async def on_ready():
    print(f'{client.me.name} has connected to Discord!')


@client.event
async def on_message_create(message):
	if message.content[0:len(":clear")] == ":clear":
		amount = message.content[len(":clear"):] 
		channel = await message.get_channel()
		await channel.purge(int(amount)+1)

	if message.content[0:len("O/a primeiro/a a clicar no butão foi o/a")] == "O/a primeiro/a a clicar no butão foi o/a":
		global state
		if state:
			state = False
			channel = await message.get_channel()
			ctn = message.content
			await channel.purge(2)
			await channel.send(ctn)
			state = False

	# Comandos com o prefixo de rpg ( ? )
	if message.content[0:comprimento] == PREFIXO_RPG:
		if message.content[1:] == "butao":
			await butao(message, interactions)
			state = True

		if message.content[comprimento:len(message.content)] == "list":
			channel = await message.get_channel()
			await channel.send("ei de fazer aqui a lista hehe")
		




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

@client.command(
		name="veritatis",
		description="Pesquisa na Wiki do Ordem sobre o assunto",
		scope=GUILD_ID
	)
@interactions.option("Assunto")
async def ordem(ctx: interactions.CommandContext, assunto: str):
	await ctx.send("https://ordemparanormal.fandom.com/wiki/"+ str(assunto))



@client.command(
		name="energia",
		description="Escolhe uma opção aleatória de todas as 5 enviadas ()",
		scope=GUILD_ID
	)
@interactions.option("Uma das opções")
@interactions.option("Uma das opções")
@interactions.option("Uma das opções")
@interactions.option("Uma das opções")
@interactions.option("Uma das opções")
async def ordem(ctx: interactions.CommandContext, opcao1:str, opcao2:str, opcao3:str, opcao4:str, opcao5:str):
	opcaos = [opcao1, opcao2, opcao3, opcao4, opcao5]
	n = randint(0, 4)
	await ctx.send("A opção escolhida pela energia foi " + opcaos[n])




	

@client.component("btn")
async def butao_energia(ctx: interactions.ComponentContext):
    await ctx.send("O/a primeiro/a a clicar no butão foi o/a"+ ctx.user.mention)









client.start()






