from discord import Bot, Intents, Embed, Color, ApplicationContext
from discord.ext.commands import CommandNotFound
from src.guide.items import Items, ResponseType
from PaginationViews import ItemPaginationView

DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"

bot = Bot(command_prefix="!", intents=Intents.all())

@bot.event
async def on_ready():
    """
    An event listener that triggers when the bot is ready. It prints the bot's information
    and details about each guild it is a part of, including the guild name, ID, member count,
    and whether the bot has administrator permissions in that guild.
    """
    bot_info = f'Bot: {bot.user} | ID: {bot.user.id}'
    guild_info = [
        f"Guild: {guild.name} | ID: {guild.id} | Members: {guild.member_count} | Admin: {guild.get_member(bot.user.id).guild_permissions.administrator}"
        for guild in bot.guilds
    ]
    print(bot_info, *guild_info, sep='\n')

@bot.event
async def on_command_error(ctx: ApplicationContext, error):
    """
    An event listener that triggers on command errors. It sends a user-friendly message
    based on the type of error encountered. For a 'CommandNotFound' error, it instructs
    the user on how to access help. For other errors, it notifies the user of an unexpected
    error.

    Parameters:
    - ctx: ApplicationContext - The context in which the command was executed.
    - error: Exception - The error that was raised.
    """
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found. Use `/help` for the list of commands.")
    else:
        await ctx.send("An unexpected error occurred. Please try again.")

@bot.slash_command()
async def help(ctx: ApplicationContext):
    """
    A slash command that provides users with a list of available commands. It creates
    an embed with a title and a green color theme, adding fields for each command
    description.

    Parameters:
    - ctx: ApplicationContext - The context in which the command is executed.
    """
    embed = Embed(title="Help", description="List of commands", color=Color.green())
    commands = [
        ("/help",   "Shows this message"),
        ("/search", "Search for an item"),
        ("/suggestprice", "Request to suggest the price of an item")
    ]
    for name, value in commands:
        embed.add_field(name=name, value=value, inline=True)
    await ctx.respond(embed=embed)

@bot.slash_command()
async def search(ctx: ApplicationContext, item: str):
    """
    A slash command that allows users to search for an item. It uses the Items class
    to perform the search and handles different types of responses (e.g., no items found,
    exact match, multiple matches) by sending appropriate embed messages or pagination views.

    Parameters:
    - ctx: ApplicationContext - The context in which the command is executed.
    - item: str - The name of the item to search for.
    """
    await ctx.defer()
    
    try:
        response = Items().searchItem(item)

        if response.r_type == ResponseType.NULL:
            await ctx.respond(embed=Embed(title=":x: Error", description="No items found!", color=Color.red()))
        elif response.r_type in {ResponseType.EXACT, ResponseType.EXTRA}:
            if response.r_type == ResponseType.EXACT:
                embed = Embed(title=f":mag: {response.results.name}", color=Color.blue())
                
                embed.add_field(name=":id: ID",     value=response.results.id,    inline=True)
                embed.add_field(name=":moneybag: Price",  value=response.results.price  if str(response.results.price)  not in ["0"] else "N/A", inline=True)
                embed.add_field(name=":arrows_counterclockwise: Update", value=response.results.update if str(response.results.update) not in ["0"] else "N/A", inline=True)
                
                embed.set_thumbnail(url=response.results.url)
                
                await ctx.respond(embed=embed)
            else:
                view = ItemPaginationView(ctx, response.results)
                await ctx.respond(embed=view.get_embed(), view=view)
    except Exception as e:
        await ctx.respond(embed=Embed(title=":x: Error", description=str(e), color=Color.red()))

@bot.slash_command()
async def suggestprice(ctx: ApplicationContext, item_id: str, new_price: str):
    """
    A slash command that allows users to change the price of an item. It uses the Items class
    to perform the change and sends an embed message to notify the user of the result.

    Parameters:
    - ctx: ApplicationContext - The context in which the command is executed.
    - item_id: str - The ID of the item to change the price for.
    - new_price: str - The new price to set for the item.
    """
    await ctx.defer()
    
    try:
        Items().changePrice(item_id, new_price)
        await ctx.respond(embed=Embed(title=":white_check_mark: Success", description="Price Suggested Successfully", color=Color.green()))
    except Exception as e:
        await ctx.respond(embed=Embed(title=":x: Error", description=str(e), color=Color.red()))

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)