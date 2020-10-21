import discord
from discord.ext import commands, tasks

from Scraper.Driver import TennoDriver
from Scraper.arbiManager import ArbiManager


class MyBot(commands.Bot):
    driver = TennoDriver()
    key = 'NzY2ODkxMTY1MTkwNDU1MzM2.X4p9DQ.wajExyD_YbsPvoLw84JYhp7gEMs'

    def __init__(self, command_prefix="!", testing=False, **options):
        super().__init__(command_prefix, **options)
        if testing:
            self.key = 'NjA0OTAyMzA2NzA5NzY2MTU0.XT0tLA.pAgvnSUh5AA_I-VIW0vAJbN-Gdc'
        self.loadCogs(self.driver, testing)

    def begin(self):
        self.run(self.key)

    def loadCogs(self, driver, testing):
        self.add_cog(arbiCommands(self, driver, testing))

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
    def __init__(self, bot, driver, testing=False):
        self.bot = bot
        self.driver = driver
        self.arbi = ArbiManager()
        if testing:
            self.channID = '604313671019266051'
            self.channID2 = self.channID
        else:
            self.channID = '766900390154862602'
            self.channID2 = '768361513035235348'
        self.checkArbi.start()

    @tasks.loop(seconds=5.0)
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

        # Always ask is this a new Arbi
        node = self.arbi.grabArbi(self.driver)
        if node is not None:
            await self.postArbi(node)

    async def postArbi(self, node):
        botChannel = await self.bot.fetch_channel(self.channID2)
        retVal = "```Current Arbitration Information" + '\n__________________________________________\n\n'
        retVal = retVal + "Node: " + node.name
        retVal = retVal + "\nEnemy Type: " + node.faction
        retVal = retVal + "\nType: " + node.mode + "```"
        await botChannel.send(retVal)

    @commands.command()
    async def Arbi(self, ctx):
        arbiData = self.driver.getArbi()
        if arbiData is None:
            await ctx.send("```Current Arbitration data is still being parsed, check back later u lil bitch muffin```")
        else:
            retVal = "```Current Arbitration Information" + '\n__________________________________________\n\n'
            retVal = retVal + "Node: " + arbiData['node']
            retVal = retVal + "\nEnemy Type: " + arbiData['enemy']
            retVal = retVal + "\nType: " + arbiData['type'] + "\n"
            alert = self.arbi.getAlert()
            if alert is None:
                retVal += "Alert Level: NONE"
            else:
                retVal += "Alert Level: " + alert
            retVal += "```"
            await ctx.send(retVal)

    @commands.command()
    async def arbi(self, ctx):
        await self.Arbi(ctx)

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
