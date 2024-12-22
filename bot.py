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

load_dotenv("./modules/.env")

TOKEN = (os.getenv("TOKEN1") + os.getenv("TOKEN2"))
PREFIXO_STAFF = ":"
PREFIXO_RPG = "?"


with open("id.json","r") as f:
    ids:dict = json.load(f)
    GUILD_IDS:list[int] = ids["GUILD_ID"]
    ROLE_DEUS_DA_MORTE:list[int] = ids["ROLE_DEUS_DA_MORTE"]
    ROLE_MANANCIAL:list[int] = ids["ROLE_MANANCIAL"]

comprimento = len(PREFIXO_RPG)

logging.basicConfig()
cls_log = logging.getLogger("MyLogger")
cls_log.setLevel(logging.DEBUG)

client = interactions.Client(
    intents=interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT | interactions.Intents.GUILD_MEMBERS,
    #sync_interactions=True,
    asyncio_debug=True,
    #logger=cls_log,
    token=TOKEN)

@prefixed_command(name="my_command")
async def my_command_function(ctx: PrefixedContext):
    await ctx.message.delete()
    await ctx.send("Hello world!")




@interactions.listen()  
async def on_ready():
    print("Ready")
    #print(client.application_commands)
    print(f"This bot is owned by {client.owner}")
    

@interactions.listen()
async def on_message_create(event: MessageCreate):
    if event.message.author.id != client.user.id:
        print(f"message received: {event.message.content}")
        
        for r_id in ROLE_MANANCIAL:
            role_manancial = event.message.guild.get_role(r_id)
            if role_manancial != None:
                break
        for r_id2 in ROLE_DEUS_DA_MORTE:
            role_deus_da_morte = event.message.guild.get_role(r_id2)
            if role_deus_da_morte != None:
                break
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






async def prefix(client:interactions.Client, message:interactions.Message):
      if message.guild.id in GUILD_IDS:
            return PREFIXO_STAFF



client.load_extension("modules.anfitriao")
client.load_extension("modules.component_helper")
client.load_extension("modules.app_commands")
client.load_extension("modules.deus_da_morte")
client.load_extension("modules.magistrado")
#prefixed_commands.setup(client, generate_prefixes=prefix)
client.start()







