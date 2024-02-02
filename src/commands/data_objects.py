import discord

class CommandHandler():
    data:           str
    cmd:            str
    args:           list[str]
    cmd_args_len:   int
    def __init__(self, c, d: str):
        self.data = d
        self.args = d.split(" ")
        self.cmd = self.args[0]
        self.cmd_args_len = len(self.args)
        self.client = c

async def help(c: CommandHandler):
    msg = f"Welcome: <@{c.auther.id}>\n\n``#help`` for a list of commands\n``#ym`` to search for items\n\tUsage: #ym <item_name_or_ID>"
    await c.client.channel.send(msg)