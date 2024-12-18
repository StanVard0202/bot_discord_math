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

    @listen()
    async def on_command_error(self,event: CommandError):
        print("hi :(",event)#TODO melhorar este handling


class Components():
    butao_producao = Button(
        custom_id="butao_producao",
        style=ButtonStyle.DANGER,
        label="Butao")

    

def setup(client):
    Component_Helper(client)