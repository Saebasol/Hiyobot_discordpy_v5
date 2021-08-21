import discord
from discord.ext import commands
from discord.ext.commands.context import Context

from hiyobot.bot import Hiyobot
from utils.paginator import Paginator


class Help(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.command(name="도움말", aliases=["help", "도움", "commands", "명령어"])
    async def _help(self, ctx: Context):
        command_list = [
            i for i in self.bot.commands if i.help if "jishaku" not in i.name
        ]

        embed_list = []

        for command in command_list:
            embed = discord.Embed(
                title="도움말",
                description=f"접두사: ``{self.bot.command_prefix}``",
                color=discord.Color.blue(),
            )

            embed.add_field(
                name=command.name,
                value=command.help,
                inline=False,
            )
            embed.set_footer(
                icon_url="https://i.imgur.com/vzwnAsf.png",
                text="https://discord.gg/PSshFYr",
            )

            embed_list.append(embed)

        await ctx.send(embed=embed_list[0], view=Paginator(ctx.author.id, embed_list))


def setup(bot: Hiyobot):
    bot.add_cog(Help(bot))
