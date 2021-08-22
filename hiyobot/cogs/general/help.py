from discord.ext import commands
from discord.ext.commands.context import Context

from hiyobot.bot import Hiyobot
from utils.general import General
from utils.paginator import Paginator


class Help(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot
        self.general = General(bot)

    @commands.command(name="도움말", aliases=["help", "도움", "commands", "명령어"])
    async def _help(self, ctx: Context):
        embed_list = self.general.make_command_embed_list()

        await ctx.send(embed=embed_list[0], view=Paginator(ctx.author.id, embed_list))


def setup(bot: Hiyobot):
    bot.add_cog(Help(bot))
