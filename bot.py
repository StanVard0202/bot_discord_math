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
from dotenv import load_dotenv
from interactions.api.events import Component, MessageCreate, CommandError
from interactions.ext.prefixed_commands import prefixed_command, PrefixedContext

load_dotenv()

TOKEN = (os.getenv("TOKEN1") + os.getenv("TOKEN2"))
GUILD_IDS = json.loads(os.getenv("GUILD_ID"))
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

@prefixed_command(name="my_command")
async def my_command_function(ctx: PrefixedContext):
    await ctx.message.delete()
    await ctx.send("Hello world!")




@interactions.listen()  
async def on_ready():
    print("Ready")
    print(client.application_commands)
    print(f"This bot is owned by {client.owner}")

@interactions.listen()
async def on_message_create(event: MessageCreate):
    if event.message.author.id != client.user.id:
        print(f"message received: {event.message.content}")
    


    





async def prefix(client:interactions.Client, message:interactions.Message):
      if message.guild.id in GUILD_IDS:
            return PREFIXO_STAFF


butao_energia_component = 1



client.load_extension("anfitriao")
client.load_extension("component_helper")
client.load_extension("app_commands")
prefixed_commands.setup(client, generate_prefixes=prefix)
client.start()







