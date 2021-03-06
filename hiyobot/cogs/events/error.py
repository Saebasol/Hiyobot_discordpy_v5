from discord.ext.commands import Cog
from discord.ext.commands.context import Context
from discord.ext.commands.errors import (
    BadArgument,
    CommandNotFound,
    MissingRequiredArgument,
    NSFWChannelRequired,
    NotOwner,
    TooManyArguments,
)

from hiyobot.bot import Hiyobot


class Error(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(
                "명령어를 찾을 수 없습니다. `&도움말` 명령어를 사용해 전체 명령어 목록을 볼 수 있습니다.", delete_after=5
            )

        elif isinstance(error, NSFWChannelRequired):
            await ctx.send(
                "연령 제한(NSFW)이 설정된 채널에서만 사용하실 수 있습니다. 이 명령어를 사용하려면 채널 관리자가 `채널 설정 -> 연령 제한 채널`을 활성화해야 합니다.",
                delete_after=5,
            )

        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "명령어 사용법이 잘못되었습니다. 값이 부족합니다. `&도움말` 명령어를 통해 정확한 사용법을 보실 수 있습니다.",
                delete_after=5,
            )

        elif isinstance(error, BadArgument):
            await ctx.send(
                "명령어 사용법이 잘못되었습니다. 지정한 값이 잘못되었습니다. `&도움말` 명령어를 통해 정확한 사용법을 보실 수 있습니다.",
                delete_after=5,
            )
        elif isinstance(error, NotOwner):
            await ctx.send("해당 명령어는 봇 관리자만 사용 가능합니다.", delete_after=5)
        elif isinstance(error, TooManyArguments):
            await ctx.send(
                "명령어의 인자값이 너무 많습니다. '&도움말' 명령어를 통해 정확한 사용법을 확인해주세요.", delete_after=5
            )
        else:
            await ctx.send(
                "알수없는 오류가 발생했습니다. 자동으로 개발자에게 오류로그를 전송합니다.\n``&문의``를 이용해 버그신고를 해주시면 더 빠른 도움이됩니다.",
                delete_after=10,
            )
            raise error


def setup(bot: Hiyobot):
    bot.add_cog(Error(bot))
