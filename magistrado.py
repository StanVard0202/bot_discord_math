import interactions, time, json, os, asyncio
from dotenv import load_dotenv
from component_helper import Components
from interactions import *

load_dotenv()

GUILD_IDS:list[int] = json.loads(os.getenv("GUILD_ID"))
ROLE_MAGISTRADO:list[int] = json.loads(os.getenv("ROLE_MAGISTRADO"))
ROLE_MASCARA:list[int] = json.loads(os.getenv("ROLE_MASCARA"))
#falta setup

def check_role(ctx:SlashContext,user:interactions.models.discord.user.Member, roles:list):
    for role_id in roles:
        role = ctx.guild.get_role(role_id)
        if role != None:
            if user.has_role(role):
                return True
    else:
        return False

class Magistrado(Extension):
    def __init__(self, bot):
        self.bot = bot
        self.vazio_channel:GuildText = None
        self.permission = False
        self.role_preso:Role = None
        print("magistrado loaded")
    @slash_command(
        name="vazio_desespero",
        description="[Magistrado]Puxa o <usuário> para o Vazio do Desespero",
        scopes=GUILD_IDS)
    @slash_option(
        name="user",
        description="Usuário a ser adicionado",
        required=False,
        opt_type=OptionType.USER)
    async def vazio(self, ctx:SlashContext, user:Member | User | None = None):
        if self.permission:
            if self.vazio_channel == None:
                self.vazio_channel = await ctx.guild.create_channel(0, "Vazio do Desespero")
                await self.vazio_channel.set_permission(ctx.guild.get_role(ctx.guild.id),view_channel=False)
                await self.vazio_channel.send("Bem vindos ao Vazio do Desespero")
                for role_id in ROLE_MAGISTRADO:
                    role = ctx.guild.get_role(role_id)
                    await self.vazio_channel.set_permission(ctx.guild.get_role(role),view_channel=True)

                for role_id in ROLE_MASCARA:
                    role = ctx.guild.get_role(role_id)
                    await self.vazio_channel.set_permission(ctx.guild.get_role(role),view_channel=True)
                if user != None:
                    await self.vazio_channel.set_permission(user,view_channel=True)

                await ctx.send("Vazio do Desespero criado com sucesso", ephemeral=True)
            elif self.vazio_channel.id == ctx.channel.id:
                await self.vazio_channel.send("O Vazio do desespero será dissipado em 20 segundos")
                await asyncio.sleep(20)
                await self.vazio_channel.delete()
                self.vazio_channel = None
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @vazio.pre_run
    async def command_pre_run(self, ctx:SlashContext, user:Member | User | None=None):
        if check_role(ctx,ctx.author,ROLE_MAGISTRADO):
            self.permission = True
#-------------------------------------------------------------------------------------------------
    @slash_command(#TODO Testar
        name="prisao_sombras",
        description="[Magistrado]Leva o <usuário> para Vazio do Desespero, impedindo que veja outros canais por <tempo>",
        scopes=GUILD_IDS)
    @slash_option(
        name="user",
        description="Usuário a ser adicionado",
        required=True,
        opt_type=OptionType.USER)
    @slash_option(
        name="tempo",
        description="Duraçao da prisao(tempo=0:indefinido(até o comando ser utilizado outra vez no canal))",
        required=False,
        opt_type=OptionType.INTEGER)
    async def prisao(self, ctx:SlashContext, user:Member | User, tempo:int=-1):
        if self.permission:
            if self.vazio_channel is None:
                self.vazio_channel = await ctx.guild.create_channel(0, "Vazio do Desespero")
                await self.vazio_channel.set_permission(ctx.guild.get_role(ctx.guild.id),view_channel=False)
                await self.vazio_channel.send("Bem vindos ao Vazio do Desespero")

                for role_id in ROLE_MAGISTRADO:
                    role = ctx.guild.get_role(role_id)
                    await self.vazio_channel.set_permission(ctx.guild.get_role(role),view_channel=True)

                for role_id in ROLE_MASCARA:
                    role = ctx.guild.get_role(role_id)
                    await self.vazio_channel.set_permission(ctx.guild.get_role(role),view_channel=True)

            if self.role_preso == None:
                self.role_preso = await ctx.guild.create_role("preso",color=0)

                for c in ctx.guild.channels:
                    await c.set_permission(self.role_preso,view_channel=False)

                await user.add_role(self.role_preso)
                await self.vazio_channel.set_permission(user,view_channel=True, send_messages=False, send_messages_in_threads=False)

                await ctx.send("Prisão das Sombras criada com sucesso", ephemeral=True)

            if tempo == -1:
                await self.vazio_channel.send(f"{user.mention} será removido em 10 segundos")
                await asyncio.sleep(10)
                await user.remove_role(self.role_preso)
                await self.vazio_channel.set_permission(user,view_channel=False)
                await self.vazio_channel.send("O Vazio do desespero será dissipado em 20 segundos")
                await asyncio.sleep(20)
                await self.vazio_channel.delete()
                self.vazio_channel = None

            elif tempo == 0:
                await self.vazio_channel.send("Para libertar o preso invocar o mesmo comando neste canal sem indicaçao de tempo")

            elif tempo>= 20:
                await self.vazio_channel.send(f"Faltam {tempo} segundos para {user.mention} ser libertado")
                await asyncio.sleep(tempo-10)
                await self.vazio_channel.send(f"{user.mention} será removido em 10 segundos")
                await asyncio.sleep(10)
                await self.vazio_channel.set_permission(user,view_channel=False)
                await user.remove_role(self.role_preso)
                await self.vazio_channel.send("O Vazio do desespero será dissipado em 20 segundos")
                await asyncio.sleep(20)
                await self.vazio_channel.delete()
                self.vazio_channel = None
            else:
                await self.vazio_channel.send(f"Faltam {tempo} segundos para {user.mention} ser libertado")
                await asyncio.sleep(tempo)
                await self.vazio_channel.set_permission(user,view_channel=False)
                await user.remove_role(self.role_preso)
                await self.vazio_channel.send("O Vazio do desespero será dissipado em 20 segundos")
                await asyncio.sleep(20)
                await self.vazio_channel.delete()
                self.vazio_channel = None
                    
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @prisao.pre_run
    async def command_pre_run(self, ctx:SlashContext, user:Member | User | None=None):
        if check_role(ctx,ctx.author,ROLE_MAGISTRADO):
            self.permission = True
#-------------------------------------------------------------------------------------------------
    @slash_command(
        name="ocultar_lembranca",
        description="[Magistrado]Apaga uma <msg> para sempre",
        scopes=GUILD_IDS)
    @slash_option(
        name="mensagem",
        description="ID da mensagem a ser apagada",
        required=True,
        opt_type=OptionType.INTEGER,
        argument_name="msg")
    async def ocultar(self, ctx:SlashContext, msg:int):
        if self.permission:
            message = ctx.channel.get_message(msg)
            await message.delete()
            await ctx.send(f"A mensagem '{message.content}' de {message.author} foi apagada", ephemeral=True)
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @ocultar.pre_run
    async def command_pre_run(self, ctx:SlashContext, msg):
        if check_role(ctx,ctx.author,ROLE_MAGISTRADO):
            self.permission = True
