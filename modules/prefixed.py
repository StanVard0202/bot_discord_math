from interactions import *


class prefixed_commands(Extension):
	def __init__(self, bot):
		self.bot = bot
		print("prefixed commands loaded")
		