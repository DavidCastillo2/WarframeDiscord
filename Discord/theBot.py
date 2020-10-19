import discord
from discord.ext import commands, tasks

from Scraper.Driver import TennoDriver
from Scraper.arbiManager import ArbiManager


class MyBot(commands.Bot):
    driver = TennoDriver()
    key = 'NzY2ODkxMTY1MTkwNDU1MzM2.X4p9DQ.wajExyD_YbsPvoLw84JYhp7gEMs'

    def __init__(self, command_prefix="!", **options):
        super().__init__(command_prefix, **options)
        self.loadCogs(self.driver)

    def begin(self):
        self.run(self.key)

    def loadCogs(self, driver):
        self.add_cog(arbiCommands(self, driver))

    async def on_ready(self):
        # Load stupid fucking cuckload opus library
        if discord.opus.is_loaded():
            print('Logged in as ' + self.user.name + "\n\n")
            return
        try:
            discord.opus._load_default()
            print('Logged in as ' + self.user.name + "\n\n")
            return
        except OSError:
            pass
            print('\n\nERROR\n\nLogged in as ' + self.user.name + "\n\n")


class arbiCommands(commands.Cog):
    def __init__(self, bot, driver):
        self.bot = bot
        self.driver = driver
        self.arbi = ArbiManager()
        self.channID = '766900390154862602'
        self.checkArbi.start()

    @tasks.loop(seconds=2.0)
    async def checkArbi(self):
        self.arbi.tick(self.driver)
        alert = self.arbi.getAlert()
        if alert is not None:
            botChannel = await self.bot.fetch_channel(self.channID)
            arbiData = self.driver.getArbi()
            retVal = "```YO, there is an active arbitration whose priority is: '" + alert + "'\n\n\n"
            retVal += "Current Arbitration Information" + '\n__________________________________________\n\n'
            retVal = retVal + "Node: " + arbiData['node']
            retVal = retVal + "\nEnemy Type: " + arbiData['enemy']
            retVal = retVal + "\nType: " + arbiData['type'] + "```"
            await botChannel.send(retVal)

    @commands.command()
    async def getArbi(self, ctx):
        arbiData = self.driver.getArbi()
        if arbiData is None:
            await ctx.send("```Current Arbitration data is still being parsed, check back later u lil bitch muffin```")
        else:
            retVal = "```Current Arbitration Information" + '\n__________________________________________\n\n'
            retVal = retVal + "Node: " + arbiData['node']
            retVal = retVal + "\nEnemy Type: " + arbiData['enemy']
            retVal = retVal + "\nType: " + arbiData['type'] + "```"
            await ctx.send(retVal)

    @commands.command()
    async def commands(self, ctx):
        helptext = "```"
        for command in self.commands:
            helptext += f"{command}\n"
        helptext += "\nType !help command for more info on a command"
        helptext += "```"
        await ctx.send(helptext)


if __name__ == "__main__":
    b = MyBot(command_prefix="!")
    b.begin()
