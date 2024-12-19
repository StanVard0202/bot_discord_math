from interactions import *
import interactions, time, json, os
from dotenv import load_dotenv
from component_helper import Components
from exp import EXP as Exposicao

EXP = Exposicao()

load_dotenv()

GUILD_IDS:list[int] = json.loads(os.getenv("GUILD_ID"))
ROLE_DEUS_DA_MORTE:list[int] = json.loads(os.getenv("ROLE_DEUS_DA_MORTE"))
ROLE_MANANCIAL:list[int] = json.loads(os.getenv("ROLE_MANANCIAL"))

def check_role(ctx:SlashContext,user:interactions.models.discord.user.Member, roles:list):
    for role_id in roles:
        role = ctx.guild.get_role(role_id)
        if role != None:
            if user.has_role(role):
                return True
    else:
        return False

class DeusDaMorte(Extension):
    def __init__(self,bot):
        self.bot:Client = bot
        self.permission:bool = False
        self.sala_santo_berco:GuildText = None
        print("deus da morte loaded")
    
    @slash_command(
        name="distorcao_temporal",
        description="[Deus Da Morte]Coloca ou remove slow-mode de um canal",
        scopes=GUILD_IDS)
    async def distorcao(self, ctx:SlashContext):
        if self.permission:
            if ctx.channel.rate_limit_per_user == 0:
                await ctx.channel.edit(rate_limit_per_user=30)
                await ctx.send("Distorção Temporal Ativada")
            else:
                await ctx.channel.edit(rate_limit_per_user=0)
                await ctx.send("Distorção Temporal Desativada")
            self.permission = False
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @distorcao.pre_run
    async def command_pre_run(self, ctx:SlashContext):
        if check_role(ctx,ctx.author,ROLE_DEUS_DA_MORTE):
            self.permission = True
#-------------------------------------------------------------------------------------------------
    @slash_command(
        name="santo_berco",
        description="[Deus Da Morte]Cria uma sala chamada Santo Berço e coloca todos especificados nela.",
        scopes=GUILD_IDS)
    async def santo(self, ctx:SlashContext):
        if self.permission:
            if self.sala_santo_berco == None:
                everyone_role = ctx.guild.get_role(ctx.guild.id)
                channel:GuildText = await ctx.guild.create_channel(channel_type=0,name="Santo Berço")
                await channel.set_permission(everyone_role,view_channel=False)

                for role_id in ROLE_DEUS_DA_MORTE:
                    role = ctx.guild.get_role(role_id)
                    await channel.set_permission(ctx.guild.get_role(role),view_channel=True)

                await channel.send(f"Santo Berço invocado por {ctx.author.mention}")
                await ctx.send(components=Components.santo_berco_user_list, ephemeral=True)

                Components.santo_berco_channel = channel
                self.sala_santo_berco = channel
            elif ctx.channel.id == self.sala_santo_berco.id:
                await self.sala_santo_berco.delete()
                self.sala_santo_berco = None
                Components.santo_berco_channel = None

            self.permission = False
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @santo.pre_run
    async def command_pre_run(self, ctx:SlashContext):
        if check_role(ctx,ctx.author,ROLE_DEUS_DA_MORTE):
            self.permission = True
#-------------------------------------------------------------------------------------------------
    @slash_command(
        name="drenar_mananciais",
        description="[Deus Da Morte]Drena o ExP de todos os mananciais para o Deus Da Morte",
        scopes=GUILD_IDS)
    async def drenar(self, ctx:SlashContext):
        if self.permission:
            for role_id in ROLE_MANANCIAL:
                r = ctx.guild.get_role(role_id)
                if ctx.guild.get_role(role_id) != None:
                    role_manancial:Role = r
                    break
            exp_drenada = 0
            for member in role_manancial.members:#FIXME nem eu sei pq é q isto n funciona
                exp = EXP.check(member)
                #EXP.remove(member,exp)
                exp_drenada += exp 
            print(exp_drenada)

            self.permission = False
        else:
            await ctx.send("Não possui o cargo nessesário", ephemeral=True)
    @drenar.pre_run
    async def command_pre_run(self, ctx:SlashContext):
        if check_role(ctx,ctx.author,ROLE_DEUS_DA_MORTE):
            self.permission = True
#-------------------------------------------------------------------------------------------------
    @slash_command(
            name="cristais",
            description="Se o <tipo>=verde, dá ExP ao <user> do próprio, se o <tipo>=preto, transforma o <user> num manancial",
            scopes=GUILD_IDS)
    @slash_option(
        name="tipo",
        description="Verde = Dar(50Exp ou o que tiver), Preto = Manancial(custo 10ExP)",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice("Cristal Verde", "verde"),
            SlashCommandChoice("Cristal Preto", "preto")
        ]
    )
    @slash_option(
        name="user",
        description="Alvo do cristal",
        required=True,
        opt_type=OptionType.USER
    )
    async def cristais(self, ctx:SlashContext, tipo:str, user:Member | User):
        match tipo:
            case "verde":
                exp_retirado = 0
                if EXP.check(ctx.author) >= 50:
                    exp_retirado = 50
                    EXP.remove(ctx.author,exp_retirado)
                elif EXP.check(ctx.author) >= 10:
                    exp_retirado = EXP.check(ctx.author)
                    EXP.remove(ctx.author,exp_retirado)
                else:
                    await ctx.send("Exp insuficiente", ephemeral=True)
                
                if exp_retirado != 0:
                    EXP.add(user,exp_retirado)
                    await ctx.send(f"Transferencia de {exp_retirado} ExP concluida")
                    


            case "preto":
                if EXP.check(ctx.author) >=10:
                    if not check_role(ctx,user,ROLE_DEUS_DA_MORTE):
                        if not check_role(ctx,user,ROLE_MANANCIAL):
                            for role_id in ROLE_MANANCIAL:
                                r = ctx.guild.get_role(role_id)
                                if ctx.guild.get_role(role_id) != None:
                                    role_manancial:Role = r
                                    break
                            EXP.remove(ctx.author,10)
                            await user.add_role(role_manancial)
                            await ctx.send(f"{user.mention} agora é um Manancial")
                        else:
                            await ctx.send(f"{user.mention} já é um Manancial")
                    else:
                        await ctx.send(f"{user.mention}  é o Deus Da Morte")
                else:
                    await ctx.send("ExP Insuficiente", ephemeral=True)



def setup(client):
    DeusDaMorte(client)