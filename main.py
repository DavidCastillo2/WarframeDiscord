import discord

from Discord.theBot import MyBot
from discord.ext import commands
from Scraper.Driver import TennoDriver

bot = commands.Bot(command_prefix='!')
driver = TennoDriver()
key = 'NzY2ODkxMTY1MTkwNDU1MzM2.X4p9DQ.wajExyD_YbsPvoLw84JYhp7gEMs'


@bot.event
async def on_ready():
    # Load stupid fucking cuckload opus library
    if discord.opus.is_loaded():
        print('Logged in as ' + bot.user.name + "\n\n")
        return
    try:
        discord.opus._load_default()
        print('Logged in as ' + bot.user.name + "\n\n")
        return
    except OSError:
        pass
        print('\n\nERROR\n\nLogged in as ' + bot.user.name + "\n\n")


@bot.command(name="commands", description="You're fucking looking at it kiddo")
async def commands(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext += f"{command}\n"
    helptext += "\nType !help command for more info on a command"
    helptext += "```"
    await ctx.send(helptext)


@bot.command(name="getArbi", description="See what the current Warframe Arbitration is if it exists.")
async def getArbi(ctx):
    arbiData = driver.getArbi()
    if arbiData is None:
        await ctx.send("Current Arbitration data is still being parsed, check back later u lil bitch muffin")
    else:
        retVal = "```Current Arbitration Information:\n ***" + arbiData['node'] + "***"
        retVal = retVal + "\nEnemy Type: " + arbiData['enemy']
        retVal = retVal + "\nType: " + arbiData['type'] + "```"
        await ctx.send(retVal)

bot.run(key)

# warframeBot = MyBot()
