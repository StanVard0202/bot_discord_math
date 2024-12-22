from interactions import *
from interactions.api.events import Component, CommandError

class Component_Helper(Extension):
    def __init__(self, bot):
        self.bot = bot
        print("Component Handeler loaded")

    @listen()
    async def on_component(self,event: Component):
        match event.ctx.custom_id:
            case Components.butao_producao.custom_id:
                await event.ctx.message.delete()
                await event.ctx.send("O/a primeiro/a a clicar no butão foi o/a"+ event.ctx.user.mention)

            case Components.memoria_falsa_user_list.custom_id:
                for member in event.ctx.values:
                    member:Member
                    dm:DM = await member.fetch_dm()
                    msg =f"O Anfitrião de {event.ctx.guild.name} transmitiu:\n{Components.memoria_falsa_mensagem}"
                    await dm.send(msg)
                await event.ctx.send("Enviado", ephemeral=True)
            
            case Components.santo_berco_user_list.custom_id:
                for member in event.ctx.values:
                    member:Member
                    await Components.santo_berco_channel.set_permission(member, view_channel=True)
                await event.ctx.send(f"{len(event.ctx.values)} foram adicionados a {Components.santo_berco_channel.mention}.",ephemeral=True)
            

    @listen()
    async def on_command_error(self,event: CommandError):
        print("hi :( ",event)#TODO melhorar isto


class Components():
    butao_producao = Button(
        custom_id="butao_producao",
        style=ButtonStyle.DANGER,
        label="Butao")
    
    memoria_falsa_user_list = UserSelectMenu(
        custom_id="memoria_falsa_user_list",
        placeholder="Destinatários",
        min_values=1,
        max_values=10)
    
    memoria_falsa_mensagem = ""

    santo_berco_user_list = UserSelectMenu(
        custom_id="santo_berco_user_list",
        placeholder="Membros",
        min_values=1,
        max_values=15)
    
    santo_berco_channel:GuildText = None

    mente_unica_input = Modal(
        ShortText(label="Mensagem desejada", custom_id="mente_unica_input"),
        title="Mente Unica",
    )

    

def setup(client):
    Component_Helper(client)