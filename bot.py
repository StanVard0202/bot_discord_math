import os, sys, subprocess
from energia import *

state = False

packages = ["python-dotenv", "discord-py-interactions", "wikipedia"]
for i in packages:
	if False:
		subprocess.check_call([sys.executable, "-m", "pip", "install", "-U",str(i)])
	else:
		print("skipped")



import interactions, logging
from dotenv import load_dotenv
from random import randint

from interactions.api.events import Component
from interactions.ext import prefixed_commands

load_dotenv()



TOKEN = (os.getenv("TOKEN1") + os.getenv("TOKEN2"))
PREFIXO_STAFF = ":"
PREFIXO_RPG = "?"


comprimento = len(PREFIXO_RPG)

logging.basicConfig()
cls_log = logging.getLogger("MyLogger")
cls_log.setLevel(logging.DEBUG)

client = interactions.Client(
    intents=interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT,
    #sync_interactions=True,
    asyncio_debug=True,
    #logger=cls_log,
    token=TOKEN
)

@interactions.listen()  
async def on_ready():
    print("Ready")
    print(client.application_commands)
    print(f"This bot is owned by {client.owner}")

@interactions.listen()
async def on_message_create(event: interactions.api.events.MessageCreate):
    if event.message.author.id != client.user.id:
        print(f"message received: {event.message.content}")
    


@interactions.listen()
async def on_component(event: Component):
    ctx = event.ctx
    await ctx.edit_origin(content="test") #TODO ver a necessidade disto
    
@interactions.listen()
async def on_command_error(event: interactions.api.events.CommandError):
    print(event)#TODO melhorar este handling





client.load_extension("app_commands")
client.start()







