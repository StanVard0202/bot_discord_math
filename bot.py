import os, sys, subprocess

packages = ["python-dotenv", "discord-py-interactions", "wikipedia"]
for i in packages:
	if False:
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
GUILD_ID = int(906974139095605278)

comprimento = len(PREFIXO_RPG)

client = interactions.Client(TOKEN, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT)

#on ready
@client.event
async def on_ready():
    print(f'{client.me.name} has connected to Discord!')

global state
#________________________________SÓ COMANDOS______________________________

@client.event
async def on_message_create(message: interactions.api.models.message.Message):
	if message.author.id == client.me.id:  #para tratar das msg q o bot manda
		if message.content == "Quem é o primeiro?":
			global btn_message
			ctx = await message.get_channel()
			btn_message = await ctx.get_message(message.id)

			

	if message.content[0:len(":clear")] == ":clear":
		amount = message.content[len(":clear"):] 
		channel = await message.get_channel()
		await channel.purge(int(amount)+1)


	# Comandos com o prefixo de rpg ( ? )

		if message.content[comprimento:len(message.content)] == "list":
			channel = await message.get_channel()
			await channel.send("ei de fazer aqui a lista hehe")
		
#Anfitras
##produçao
@client.command(
		name="butao",
		description="Um botao aparece, e logo em seguida os primeiros a apertar aparecem no chat."
)
async def butao(ctx: interactions.CommandContext):
    button = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="BUTÃO HAHAHAHA",
        custom_id="btn",
    )
    await ctx.send("Quem é o primeiro?",components=button)
    global state
    state = True


#Comandos gerais(slash)

#@client.command(name="command-name", description="this is a command.")
#async def command_name(ctx):
#    print("hi")


@client.command(
	name="ping",
	description="Devolve a latência da api do bot")
async def ping(ctx: interactions.CommandContext):
	await ctx.send(f'O bot está com uma latência de {round(client.latency, 3)} ms')



@client.command(
	name="realitas",
	description="Pesquisa na Wikipédia sobre o assunto")
@interactions.option("Assunto")
async def wiki(ctx: interactions.CommandContext, assunto: str):
	await ctx.send(wp.summary(str(assunto), sentences=1))



@client.command(
		name="veritatis",
		description="Pesquisa na Wiki do Ordem sobre o assunto")
@interactions.option("Assunto")
async def ordem(ctx: interactions.CommandContext, assunto: str):
	await ctx.send("https://ordemparanormal.fandom.com/wiki/"+ str(assunto))



@client.command(
		name="energia",
		description="Escolhe uma opção aleatória de todas as 5 enviadas ()")
@interactions.option("Uma das opções")
@interactions.option("Uma das opções")
@interactions.option("Uma das opções")
@interactions.option("Uma das opções")
@interactions.option("Uma das opções")
async def ordem(ctx: interactions.CommandContext, opcao1:str, opcao2:str, opcao3:str, opcao4:str, opcao5:str):
	opcaos = [opcao1, opcao2, opcao3, opcao4, opcao5]
	n = randint(0, 4)
	await ctx.send("A opção escolhida pela energia foi " + opcaos[n])




#components
@client.component("btn")
async def butao_energia(ctx: interactions.ComponentContext):
    await btn_message.delete()
    await ctx.send("O/a primeiro/a a clicar no butão foi o/a"+ ctx.user.mention)
    



 
client.start()





