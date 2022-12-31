def commands(CommandContext, client, GUILD_ID):
    @client.command(
        name="ping",
        description="Devolve a latência da api do bot",
        scope=GUILD_ID
    )
    async def my_first_command(ctx: CommandContext):
        await ctx.send(f'O bot está com uma latência de {round(client.latency, 3)} ms')