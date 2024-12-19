from interactions import Extension, Client, slash_command, slash_option, OptionType, SlashContext, Permissions
from dotenv import load_dotenv
from random import randint
import json, os, interactions, time
from component_helper import Components
from interactions.api.events import Component

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

class Anfitriao(Extension):
    def __init__(self, bot:Client):
        self.bot:Client = bot
        self.permission = False
        self.mensagem = ""
        print("anfitriao loaded")

    @slash_command(
            name="dado",
            description="[Anfitrião]Rola um dado de 100 lados e muta o <usuario> pelo tempo do resultado do d100(em segundos)", 
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
                await user.timeout(time.time() + time_out) 
                await ctx.send(f"{user.mention} foi mutado por {time_out} segundos")
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
            description="[Anfitrião e Produção]Um botão aparece", 
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
#-------------------------------------------------------------------------------------------------
    @slash_command(
            name="troca_troca",
            description="[Anfitrião e Produção]Troca dois usuarios de canal de voz", 
            scopes=GUILD_IDS)
    @slash_option(
        name="user1",
        description="",
        required=True,
        opt_type=OptionType.USER)
    @slash_option(
        name="user2",
        description="",
        required=True,
        opt_type=OptionType.USER)
    async def troca(self, ctx:SlashContext, user1:interactions.models.discord.user.Member, user2:interactions.models.discord.user.Member):
        if self.permission:
            channel1 = user1.voice.channel.id
            channel2 = user2.voice.channel.id
            if channel1 == None or channel2 == None:
                await ctx.send("Pelo menos um dos usuarios não está num canal de voz", ephemeral=True)
            else:
                await user1.edit(channel_id=channel2)
                await user2.edit(channel_id=channel1)
                await ctx.send("Trocados com sucesso")
            self.permission = False
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @troca.pre_run
    async def command_pre_run(self, ctx:SlashContext, user1, user2):
        if check_role(ctx,ctx.author,ROLE_PRODUCAO) | check_role(ctx,ctx.author,ROLE_ANFITRIAO):
            self.permission = True
#-------------------------------------------------------------------------------------------------
    @slash_command(
            name="memoria_falsa",
            description="[Anfitrião]Manda a mensagem para todos que o Anfitrião selecionar", 
            scopes=GUILD_IDS)
    @slash_option(
        name="mensagem",
        description="Mensagem a ser enviada",
        required=True,
        opt_type=OptionType.STRING)
    async def memoria(self, ctx:SlashContext, mensagem:str):
        if self.permission:
            await ctx.send(components=Components.memoria_falsa_user_list, ephemeral=True)
            Components.memoria_falsa_mensagem = mensagem
            self.permission = False
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @memoria.pre_run
    async def command_pre_run(self, ctx:SlashContext, mensagem):
        if check_role(ctx,ctx.author,ROLE_ANFITRIAO):
            self.permission = True
#-------------------------------------------------------------------------------------------------
    @slash_command(
            name="sol",
            description="[Anfitrião]Inibe a utilizaçao do chat por 2d100 segundos", 
            scopes=GUILD_IDS)
    @slash_option(
        name="mensagem",
        description="Mensagem a ser enviada",
        required=True,
        opt_type=OptionType.STRING)
    async def sol(self, ctx:SlashContext, mensagem:str):
        if self.permission:
            tempo = randint(2,200)
            ti = time.time()
            ta = 0
            await ctx.send(f"O SOL queimara por {tempo} segundos \n https://tenor.com/view/sun-waving-hi-hello-smiles-gif-15302254 ")
            
            everyone_role = ctx.guild.get_role(ctx.guild.id)

            while ta <= ti + tempo:
                await ctx.channel.set_permission(everyone_role, send_messages=False,send_messages_in_threads=False)
                ta = time.time()

            await ctx.channel.set_permission(everyone_role, send_messages=True,send_messages_in_threads=True)
            self.permission = False
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @sol.pre_run
    async def command_pre_run(self, ctx:SlashContext, mensagem):
        if check_role(ctx,ctx.author,ROLE_ANFITRIAO):
            self.permission = True

def setup(client):
    Anfitriao(client)