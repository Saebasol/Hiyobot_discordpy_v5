import discord
from discord import Embed

from hiyobot.bot import Hiyobot


class General:
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    def make_command_embed_list(self) -> list[Embed]:
        command_list = [
            i for i in self.bot.commands if i.help if "jishaku" not in i.name
        ]
        command_num = len(command_list)

        embed_list = []

        embed_num = command_num // 5 + 1
        if command_num % 5 == 0:
            embed_num -= 1

        for i in range(embed_num):
            embed = discord.Embed(
                title=f"도움말 ({i+1}/{embed_num})",
                description=f"접두사: ``{self.bot.command_prefix}``",
                color=discord.Color.blue(),
            )
            embed.set_footer(
                icon_url="https://discord.com/assets/f9bb9c4af2b9c32a2c5ee0014661546d.png",
                text=f"공식 지원 서버: {self.bot.command_prefix}지원",
            )

            for command in command_list[i * 5 : (i + 1) * 5]:
                embed.add_field(
                    name=command.name,
                    value=command.help,
                    inline=False,
                )

            embed_list.append(embed)

        return embed_list
