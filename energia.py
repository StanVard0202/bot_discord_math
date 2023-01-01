async def butao(message, interactions):
    channel = await message.get_channel()
    button = interactions.Button(
        style=interactions.ButtonStyle.PRIMARY,
        label="BUTÃO HAHAHAHA",
        custom_id="btn",
    )
    await message.delete()
    await channel.send(components=button)


