from interactions import *
import interactions
import os, json
import wikipedia as wp
from random import randint
from modules.exp import EXP as Exposicao

EXP = Exposicao()

wp.set_lang("pt")

with open("id.json","r") as f:
    ids:dict = json.load(f)
    GUILD_IDS:list[int] = ids["GUILD_ID"]

class Slash_Commands(Extension):
    def __init__(self, bot):
        self.bot:Client = bot
        print("App Commands loaded")

    @slash_command(
            name="exp",
            description="[Geral]Verifica a Exposição Paranormal de um usuario", 
            scopes=GUILD_IDS)
    @slash_option(
         name="user",
         description="Usuario",
         required=True,
         opt_type=OptionType.USER)
    async def exp(self, ctx: SlashContext, user:interactions.models.discord.user.Member ):
        if EXP.check(user) == False:
            EXP.add_user(user)
            await ctx.send(f"{user.mention} não tem Exposição Paranormal")
        else:
            await ctx.send(f"{user.mention} tem {EXP.check(user)} Exposição Paranormal")
            
#-------------------------------------------------------------------------------------------------
    @slash_command(
            name="energia",
            description="[Geral]Escolhe uma opção aleatória detre as enviadas(separadas por ;)", 
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
        choice = randint(0,len(opcoes)-1)
        await ctx.send(f"A opção escolhida pela energia foi: {opcoes[choice]}")
#-------------------------------------------------------------------------------------------------
    @slash_command(
              name="realitas",
              description="[Geral]Pesquisa na Wikipédia sobre o assunto", 
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
              description="[Geral]Pesquisa na Wiki do Ordem sobre o assunto",
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
#-------------------------------------------------------------------------------------------------
    


def setup(client):
    Slash_Commands(client)
