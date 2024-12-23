from interactions import *
from interactions.ext import prefixed_commands
from interactions.ext.prefixed_commands import prefixed_command, PrefixedContext
from dotenv import load_dotenv
import os

load_dotenv()

PREFIX = os.getenv("PREFIX")
CONFIG_USER_ID = os.getenv("CONFIG_USER_ID")

class PrefixedCommands(Extension):
	def __init__(self, bot):
		self.bot:Client = bot
		print("prefixed commands loaded")

	


def setup(client):
	PrefixedCommands(client)
	