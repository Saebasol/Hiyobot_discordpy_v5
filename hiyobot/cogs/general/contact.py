import discord
import discord
from discord.ext import commands
from discord.ext.commands.context import Context

from hiyobot.bot import Hiyobot


class Contact(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.command(name="지원", aliases=["공식디코", "지원서버"])
    async def _support(self, ctx: Context):
        embed = discord.Embed(
            title=":mailbox: 공식 디스코드 서버",
            description="[여기](https://discord.gg/PSshFYr)를 눌러주세요.",
            color=discord.Color.blue(),
        )

        await ctx.send(embed=embed)


def setup(bot: Hiyobot):
    bot.add_cog(Contact(bot))
