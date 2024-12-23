import os, sys, subprocess
from interactions.ext import prefixed_commands
state = False

packages = ["python-dotenv", "discord-py-interactions", "wikipedia"]
for i in packages:
	if False:
		subprocess.check_call([sys.executable, "-m", "pip", "install", "-U",str(i)])
	else:
		print("skipped")



import interactions, logging, json
from dotenv import load_dotenv
from random import randint
from interactions.api.events import Component, MessageCreate, CommandError
from interactions.ext.prefixed_commands import prefixed_command, PrefixedContext
from modules.exp import EXP as Exposicao

EXP = Exposicao()

load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
CONFIG_USER_ID = os.getenv("CONFIG_USER_ID")
IS_SETUP = os.getenv("IS_SETUP")

with open("id.json","r") as f:
    ids:dict = json.load(f)
    ROLE_DEUS_DA_MORTE:list[int] = ids["ROLE_DEUS_DA_MORTE"]
    ROLE_MANANCIAL:list[int] = ids["ROLE_MANANCIAL"]

logging.basicConfig()
cls_log = logging.getLogger("MyLogger")
cls_log.setLevel(logging.DEBUG)

client = interactions.Client(
    intents=interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT | interactions.Intents.GUILD_MEMBERS,
    #sync_interactions=True,
    asyncio_debug=True,
    #logger=cls_log,
    token=TOKEN)

@interactions.listen()  
async def on_ready():
    print("Ready")
    #print(client.application_commands)
    print(f"This bot is owned by {client.owner}")

   
@prefixed_command(name="ping")
async def ping(ctx: PrefixedContext):
	await ctx.send(f'O bot está com uma latência de {round(client.latency, 3)} s')

@prefixed_command(name="config")
#@interactions.check(interactions.has_id(int(CONFIG_USER_ID)))
async def config(ctx: PrefixedContext):
    if IS_SETUP == "0":
        magistrado_role = await ctx.guild.create_role("Magistrado", color=interactions.Color().from_hex("ecc900"))
        anfitriao_role = await ctx.guild.create_role("Anfitrião", color=interactions.Color().from_hex("b700ff"))
        deus_role = await ctx.guild.create_role("Deus da Morte", color=interactions.Color().from_hex("010101")) 
        producao_role = await ctx.guild.create_role("Produção", color=interactions.Color().from_hex("d05aff"))
        mascara_role = await ctx.guild.create_role("Mascara", color=interactions.Color().from_hex("d8a500"))
        manancial_role = await ctx.guild.create_role("Manancial", color=interactions.Color().from_hex("141414"))
        
        with open("id.json","r") as f:
            ids:dict = json.load(f)
            GUILD_ID:list[int] = ids["GUILD_ID"]
            ROLE_ANFITRIAO:list[int] = ids["ROLE_ANFITRIAO"]
            ROLE_PRODUCAO:list[int] = ids["ROLE_PRODUCAO"]
            ROLE_DEUS_DA_MORTE:list[int] = ids["ROLE_DEUS_DA_MORTE"]
            ROLE_MANANCIAL:list[int] = ids["ROLE_MANANCIAL"]
            ROLE_MAGISTRADO:list[int] = ids["ROLE_MAGISTRADO"]
            ROLE_MASCARA:list[int] = ids["ROLE_MASCARA"]

        GUILD_ID.append(ctx.guild_id)
        ROLE_ANFITRIAO.append(anfitriao_role.id)
        ROLE_PRODUCAO.append(producao_role.id)
        ROLE_DEUS_DA_MORTE.append(deus_role.id)
        ROLE_MANANCIAL.append(manancial_role.id)
        ROLE_MAGISTRADO.append(magistrado_role.id)
        ROLE_MASCARA.append(mascara_role.id)

        with open("id.json","w") as f:
            dic:dict = {
                "GUILD_ID" : GUILD_ID,
                "ROLE_ANFITRIAO" : ROLE_ANFITRIAO,
                "ROLE_PRODUCAO" : ROLE_PRODUCAO,
                "ROLE_DEUS_DA_MORTE" : ROLE_DEUS_DA_MORTE,
                "ROLE_MANANCIAL" : ROLE_MANANCIAL,
                "ROLE_MAGISTRADO" : ROLE_MAGISTRADO,
                "ROLE_MASCARA" : ROLE_MASCARA
            }
            json.dump(dic,f)
        await ctx.send("Servidor configurado com sucesso")
        await ctx.send(f"Anfitrião:{anfitriao_role.mention},{anfitriao_role.color.hex}\nProdução:{producao_role.mention},{producao_role.color.hex}\nDeus da Morte:{deus_role.mention},{deus_role.color.hex}\nManancial:{manancial_role.mention},{manancial_role.color.hex}\nMagistrado:{magistrado_role.mention},{magistrado_role.color.hex}\nMascara:{mascara_role.mention},{mascara_role.color.hex}")
    else:
        await ctx.send("O servidor já foi configurado")

@interactions.listen()
async def on_message_create(event: MessageCreate):
    if event.message.author.id != client.user.id:
        print(f"message received: {event.message.content}")
        r = False
        
        for r_id in ROLE_MANANCIAL:
            role_manancial = event.message.guild.get_role(r_id)
            if role_manancial != None:
                break
        for r_id2 in ROLE_DEUS_DA_MORTE:
            role_deus_da_morte = event.message.guild.get_role(r_id2)
            if role_deus_da_morte != None:
                break

        if (role_manancial == None) or (role_deus_da_morte == None):
            print("faltam configurar")
        else:
            deus_da_morte = role_deus_da_morte.members
            if role_manancial in event.message.author.roles:
                EXP.add(event.message.author,round(len(event.message.content)*0.4))
                for i in deus_da_morte:
                    EXP.add(i,round(len(event.message.content)*0.2))
                #print("manancial")
            elif role_deus_da_morte in event.message.author.roles:
                EXP.add(event.message.author,round(len(event.message.content)*0.1))
                #print("deus da morte")
            else:
                EXP.add(event.message.author,round(len(event.message.content)*0.6))
                #print("peasent")



client.load_extension("modules.anfitriao")
client.load_extension("modules.component_helper")
client.load_extension("modules.app_commands")
client.load_extension("modules.deus_da_morte")
client.load_extension("modules.magistrado")
prefixed_commands.setup(client, default_prefix=PREFIX)
client.start()







