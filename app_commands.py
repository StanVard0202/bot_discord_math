from interactions import *
import os, json
import wikipedia as wp
from dotenv import load_dotenv
from random import randint

load_dotenv()
wp.set_lang("pt")

GUILD_IDS = json.loads(os.getenv("GUILD_ID"))

class Slash_Commands(Extension):
    def __init__(self, bot):
        self.bot:Client = bot
        print("Extention Created")

    @slash_command(
            name="energia",
            description="Escolhe uma opção aleatória detre as enviadas(separadas por ;)", 
            scopes=GUILD_IDS
            )
    @slash_option(
         name="opcoes",
         description="Opções:",
         required=True,
         opt_type=OptionType.STRING
         )
    async def energia(self, ctx: SlashContext, opcoes:str ):
        opcoes = opcoes.split(";")
        print(opcoes)
        choice = randint(0,len(opcoes)-1)
        await ctx.send(f"A opção escolhida pela energia foi: {opcoes[choice]}")
#-------------------------------------------------------------------------------------------------
    @slash_command(
              name="ping",
              description="latency", 
              scopes=GUILD_IDS
              )
    async def ping(self, ctx : SlashContext):
        await ctx.send(f'O bot está com uma latência de {round(self.bot.latency, 3)} ms')
#-------------------------------------------------------------------------------------------------
    @slash_command(
              name="realitas",
              description="Pesquisa na Wikipédia sobre o assunto", 
              scopes=GUILD_IDS
              )
    @slash_option(
         name="assunto",
         description="Assunto:",
         required=True,
         opt_type=OptionType.STRING
         )
    async def wiki(self, ctx: SlashContext, assunto: str):
        try:
            await ctx.send(wp.summary(str(assunto), sentences=1))
        except:
            await ctx.send("Falta de clareza no tema ou não existente.")
#-------------------------------------------------------------------------------------------------
    @slash_command(
              name="veritatis",
              description="Pesquisa na Wiki do Ordem sobre o assunto",
              scopes=GUILD_IDS
              )
    @slash_option(
         name="assunto",
         description="Assunto:",
         required=True,
         opt_type=OptionType.STRING
         )
    async def ordem(self,ctx: SlashContext, assunto: str):
	    await ctx.send("https://ordemparanormal.fandom.com/wiki/"+ str(assunto))
         


def setup(client):
    Slash_Commands(client)

