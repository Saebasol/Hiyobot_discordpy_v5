import discord
from discord.ext.commands.cog import Cog

import hiyobot
from hiyobot.bot import Hiyobot


class Ready(Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Login.. : ")
        if self.bot.user:
            print(self.bot.user.name)
            print(self.bot.user.id)

        game = discord.Game(f"&도움말 | {hiyobot.__version__}")
        await self.bot.change_presence(status=discord.Status.online, activity=game)


def setup(bot: Hiyobot):
    bot.add_cog(Ready(bot))
