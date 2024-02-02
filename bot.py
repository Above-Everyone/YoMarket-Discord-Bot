import discord

from src.commands.search import *
from src.commands.data_objects import *

class YoMarket_Config:
    token = "MTIwMjQ1Njg1NjcwMjc0NjY5NQ.Gu4xBG.HM1LI9NYLztoWW3T6zvfpBP4YB--PnFy2QOsas"
    prefix = "#"
    """
        Add your new command in 'commands' and 'execute_cmd' then create your file & command function to link in 'execute_cmds'
    """
    commands = {
        # "CMD" : MAX_ARGS_INT
        "help": 0,
        "ym": 1
    }

    execute_cmd = {
        # "CMD" : FUNCTION
        "help": help,
        "ym": searchCommand
    }

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
    async def on_message(self, message):
        data = message.content
        args = data.split(" ")
        cmd = args[0].replace(f"{YoMarket_Config.prefix}", "").strip()

        if f"{message.author.id}" == "1202456856702746695": return
        
        if len(args) > 0:
            if cmd in YoMarket_Config.commands:
                if data.startswith(f"{YoMarket_Config.prefix}{cmd}"):
                    if len(args) > YoMarket_Config.commands[cmd]:
                        await YoMarket_Config.execute_cmd[cmd](CommandHandler(message, data))
                        return

        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(YoMarket_Config.token)