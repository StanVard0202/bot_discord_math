from interactions import Extension, Client, slash_command, slash_option, OptionType, SlashContext
from dotenv import load_dotenv
from random import randint
import json, os, interactions, time
from component_helper import Components

load_dotenv()

GUILD_IDS:list[int] = json.loads(os.getenv("GUILD_ID"))
ROLE_ANFITRIAO:list[int] = json.loads(os.getenv("ROLE_ANFITRIAO"))
ROLE_PRODUCAO:list[int] = json.loads(os.getenv("ROLE_PRODUCAO"))

def check_role(ctx:SlashContext,user:interactions.models.discord.user.Member, roles:list):
    for role_id in roles:
        role = ctx.guild.get_role(role_id)
        if role != None:
            if user.has_role(role):
                return True
    else:
        return False


#TODO setup function
class Anfitriao(Extension):
    def __init__(self, bot:Client):
        self.bot:Client = bot
        self.permission = False
        print("anfitriao loaded")

    @slash_command(
            name="dado",
            description="Rola um dado de 100 lados e muta o <usuario> pelo tempo do resultado do d100(em segundos)", 
            scopes=GUILD_IDS)
    @slash_option(
        name="user",
        description="O caos o silenciará",
        required=True,
        opt_type=OptionType.USER)
    async def dado(self, ctx: SlashContext, user:interactions.models.discord.user.Member):
        if self.permission:
            if not(check_role(ctx,user,ROLE_ANFITRIAO)):
                time_out=randint(1,100)
                print(time_out)
                await user.timeout(time.time() + time_out) #TODO ver se isto funciona com outros membros(n é q funcione cmg)
            else:
                await ctx.send(f"{user.mention} tem um cargo superior")
            self.permission = False
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @dado.pre_run
    async def command_pre_run(self, ctx:SlashContext, user):
        self.permission = check_role(ctx,ctx.author,ROLE_ANFITRIAO)
#-------------------------------------------------------------------------------------------------
    @slash_command(
            name="butao",
            description="Um botão aparece", 
            scopes=GUILD_IDS)
    async def butao(self, ctx:SlashContext):
        if self.permission:
            await ctx.send(components=Components.butao_producao)
            self.permission = False
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @butao.pre_run
    async def command_pre_run(self, ctx:SlashContext):
        if check_role(ctx,ctx.author,ROLE_PRODUCAO) | check_role(ctx,ctx.author,ROLE_ANFITRIAO):
            self.permission = True



def setup(client):
    Anfitriao(client)