import os, sys, subprocess, random , time

packages = ["python-dotenv", "discord-py-interactions", "wikipedia"]
for i in packages:
	if False:
		subprocess.check_call([sys.executable, "-m", "pip", "install", "-U",str(i)])
	else:
		print("skipped")


import interactions
from interactions import listen, slash_command, slash_option, slash_default_member_permission, OptionType
from interactions.api.events import Startup, MessageCreate, Component
from dotenv import load_dotenv
import wikipedia as wp

load_dotenv()

wp.set_lang("pt")

TOKEN = (os.getenv("TOKEN1") + os.getenv("TOKEN2"))
PREFIXO_STAFF = ":"
PREFIXO_RPG = "?"
GUILD_ID = int(906974139095605278)

comprimento = len(PREFIXO_RPG)

client = interactions.Client(token=TOKEN, intents=interactions.Intents.DEFAULT | interactions.Intents.GUILDS | interactions.Intents.GUILD_INVITES)

#on ready
@listen(Startup)
async def startup_function():
    print("Ready")
    print(f"This bot is {client.user.display_name}")
    print(f"This bot is owned by {client.owner}")
		
		    

global state
global btn_energia_id

#________________________________IDs______________________________
role_anfitriao_id:int = 0
role_produçao_id:int = 1145355943706640394
role_mutted:int = 1145444177736368218

#________________________________SÓ COMANDOS______________________________

@listen(MessageCreate)#Message handeler
async def on_message_create(event: MessageCreate):
	message = event.message
	if message.author.id == client.user.id:  #para tratar das msg q o bot manda
		if message.content == "Quem é o primeiro?":
			global btn_energia_id
			btn_energia_id = message.id


		

#Comandos gerais
if False: #Comando de Clear
	@interactions.is_owner()
	@slash_command(
			name="clear",
			description="Limpa nº mensagens do chat")
	@slash_default_member_permission(interactions.Permissions.MANAGE_MESSAGES)
	@slash_default_member_permission(interactions.Permissions.MANAGE_CHANNELS)
	@slash_option(
	name="n",
	description="Numero de mensagens a apagar",
    required=True,
    opt_type=OptionType.INTEGER)
	async def clear(ctx:interactions.SlashContext, n:int):
		await ctx.channel.purge(n)
		await ctx.send(ctx.user.mention + " o chat foi limpo", ephemeral=True)


@slash_command(
	name="ping",
	description="Devolve a latência da api do bot",
	group_name="geral")
async def ping(ctx: interactions.SlashContext):
	await ctx.send(f'O bot está com uma latência de {round(client.latency, 3)} ms')



@slash_command(
	name="realitas",
	description="Pesquisa na Wikipédia sobre o assunto",
	group_name="geral")

@slash_option(
	name="assunto",
	description="Assunto",
    required=True,
    opt_type=OptionType.STRING
)
async def wiki(ctx: interactions.SlashContext, assunto: str):
	await ctx.send(wp.summary(str(assunto), sentences=1))



@slash_command(
		name="veritatis",
		description="Pesquisa na Wiki do Ordem sobre o assunto",
		group_name="geral")
@slash_option(
	name="assunto",
	description="Assunto",
    required=True,
    opt_type=OptionType.STRING
)
async def ordem(ctx: interactions.SlashContext, assunto: str):
	message = "https://ordemparanormal.fandom.com/wiki/"+ str(assunto)
	await ctx.send((message))

@slash_command(
		name="energia",
		description="Escolhe uma opção aleatória de todas enviadas (separadas por ,) ",
		group_name="geral")
@slash_option(
	name="opcao",
	description="Opções separadas por ,",
    required=True,
    opt_type=OptionType.STRING
)
async def ordem(ctx: interactions.SlashContext, opcao:str):
	opcao2 = opcao.split(",")
	choice = random.randint(0, len(opcao2)-1)
	m = "A escolha do caos foi: "+ str(opcao2[choice])
	await ctx.send(m)




#Anfitras
@slash_command(
		name="dado_de_100",
		description="[Anfitrião]Rola um dado de 100 lados e muta o <úsuario> pelo tempo do resultado do dado de 100",
		group_name="anfitiao"
)
@slash_option(
	name="usuario",
	description="Usuario a ser mutado",
    required=True,
    opt_type=OptionType.STRING
)
async def dado_de_100(ctx: interactions.SlashContext, usuario:interactions.Member):
	r = random.randint(1,100)
	duration = r + time.time()
	if not(await check_role(ctx, role_anfitriao_id)):
		await ctx.send("Tu não tens permissao para isso HAHA")
	else:
		await ctx.send(str(duration))
		await usuario.timeout(duration)


#


@slash_command(
		name="memoria_falsa",
		description="Manda a msg para todos que o Anfitrião selecionar (<...>)",
		group_name="anfitiao"
)
@slash_option(
	name="msg",
	description="mensagem a ser enviada",
	required=True,
	opt_type=OptionType.STRING
)
@slash_option(
	name="user",
	description="Usuarios a receberem a msg",
	required=True,
	opt_type=OptionType.MENTIONABLE
)
async def memoria_falsa(ctx: interactions.SlashContext, msg:str, user: interactions.User):
	await user.send(msg)
	await ctx.send(f"' {msg} ' foi mandado para {user}",ephemeral=True)


##produçao
@slash_command(
		name="butao",
		description="[Anfitrião, Produção]Um botao aparece, e logo em seguida os primeiros a apertar aparecem no chat.",
		group_name="anfitrião_produção"
)
async def butao(ctx: interactions.SlashContext):
	button = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="BUTÃO HAHAHAHA",
        custom_id="btn_energia",
    )
	if not((await check_role(ctx , role_produçao_id)) or (await check_role(ctx, role_anfitriao_id))):
		await ctx.send("Tu não tens permissao para isso HAHA")
	else:
		await ctx.send("Quem é o primeiro?",components=button)









#______________________________________components________________________
@listen()
async def on_component(event: Component):
    global btn_energia_id
    ctx = event.ctx

    match ctx.custom_id:
        case "btn_energia":
            await butao_energia(ctx, btn_energia_id)
	    


async def butao_energia(ctx: interactions.ComponentContext, btn_id:interactions.Snowflake):
	await ctx.channel.delete_message(btn_id)
	await ctx.send("O/a primeiro/a a clicar no butão foi o/a"+ ctx.user.mention)

    

#______________________________Functions____________________________________

async def check_role(ctx: interactions.SlashContext, target_id):
	for i in ctx.author.roles:
		if i == target_id:
			return True
	else:
		return False


async def get_role_id(ctx:interactions.SlashContext, name:str):
	for r in await ctx.guild.get_all_roles():
		if r.name == name:
			return r.id
			

 
client.start()


#TODO fazer o comando de lista dos comandos de acordo com as roles
#TODO acabar o d100 com o timeout
#TODO ver a parte de group dos novos slash commands


# ephemeral=True para fazer com q só quem mandou o comando veja a resposta
# ctx.author.send() para mandar uma dm

