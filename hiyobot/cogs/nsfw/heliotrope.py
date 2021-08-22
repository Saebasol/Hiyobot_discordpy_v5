from discord import Embed
from discord.ext import commands

from hiyobot.bot import Hiyobot
from utils.paginator import Paginator


class Heliotrope(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.group("heliotrope")
    @commands.command("번호")
    @commands.is_nsfw()
    async def _info(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 히토미에서 해당 작품 정보를 가져옵니다.
        사용할 수 있는 값 : 작품 번호(필수)
        사용 예시 : ``&번호 1867978``
        """

        message = await ctx.send(embed=Embed(title="정보를 요청합니다. 잠시만 기다려주세요."))

        if embed := await self.bot.mintchoco.gallery_info(index):
            return await message.edit(embed=embed)

        await message.edit(embed=Embed(title="정보를 찾지 못했습니다."))

    @commands.group("heliotrope")
    @commands.command("검색")
    @commands.is_nsfw()
    async def _search(self, ctx: commands.Context, *, query: str):
        """
        검색을 요청합니다.
        """

        message = await ctx.send(embed=Embed(title="정보를 요청합니다. 잠시만 기다려주세요."))

        if embeds := await self.bot.mintchoco.gallery_search(query.split(" ")):
            return await message.edit(embed=embeds[0], view=Paginator(ctx.author.id, embeds))

        await message.edit(embed=Embed(title="정보를 찾지 못했습니다."))

    @commands.group("heliotrope")
    @commands.command("리스트")
    @commands.is_nsfw()
    async def _list(self, ctx: commands.Context, num: int = 1):
        """
        히토미에서 최근 올라온 한국어 작품을 가져옵니다.
        사용할 수 있는 값 : 페이지(입력하지 않을 경우 1)
        사용 예시 : ``&리스트`` 또는 ``&리스트 2``
        """

        message = await ctx.send(embed=Embed(title="정보를 요청합니다. 잠시만 기다려주세요"))

        if embeds := await self.bot.mintchoco.gallery_list(num):
            return await message.edit(embed=embeds[0], view=Paginator(ctx.author.id, embeds))

        await message.edit(embed=Embed(title="정보를 찾지 못했습니다."))

    @commands.group("heliotrope")
    @commands.command("뷰어")
    @commands.is_nsfw()
    async def _viewer(self, ctx: commands.Context, index: int):
        """
        작품 번호를 입력하면 디스코드 내에서 보여줍니다.
        인자값: 작품 번호(필수)
        사용법: ``&뷰어 1496588``
        """

        message = await ctx.send(embed=Embed(title="정보를 요청합니다. 잠시만 기다려주세요."))

        if embeds := await self.bot.mintchoco.gallery_viewer(index):
            return await message.edit(embed=embeds[0], view=Paginator(ctx.author.id, embeds))

        await message.edit(embed=Embed(title="정보를 찾지 못했습니다."))


def setup(bot: Hiyobot):
    bot.add_cog(Heliotrope(bot))
