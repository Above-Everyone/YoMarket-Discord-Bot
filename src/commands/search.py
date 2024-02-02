import discord

from .data_objects import *
from src.guide.items import *

async def searchCommand(c: CommandHandler):
    query = c.data.replace(f"{c.args[0]}", "").strip()
    guide = Items(query)
    r = guide.searchItem(query, "5.5.5.5")

    if r.r_type == ResponseType.NULL:
        await c.client.channel.send("[ X ] Error, No items found...!")
        return
    elif r.r_type == ResponseType.EXACT:
        await c.client.channel.send(f"**{r.results.name}**\n\tID => {r.results.id}\n\tPrice => {r.results.price}\n\tUpdate => {r.results.update}")
        return
    elif r.r_type == ResponseType.EXTRA:
        data = ""
        for item in r.results:
            if len(data) > 1950: break
            data += f"{item.name} {item.price} {item.update}"

        if len(data) > 0:
            await c.client.channel.send(f"{data}")
            return

    await c.client.channel.send(f"[ X ] Invalid operation ```{c.data}\n{c.args}\n{query}```")