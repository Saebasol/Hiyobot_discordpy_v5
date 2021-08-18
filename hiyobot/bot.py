from glob import glob
from typing import Any, Optional
from utils.request import Request

from discord.ext.commands.bot import Bot
from discord.state import Intents

from utils.mintchoco import MintChoco
from utils.pixiv import Pixiv


class Hiyobot(Bot):
    def __init__(self, command_prefix: str, **options: Any):
        super().__init__(command_prefix, help_command=None, description=None, **options)
        self.mintchoco = MintChoco()
        self.pixiv = Pixiv()
        self.request = Request()

    async def close(self):
        await self.pixiv.close()
        await self.mintchoco.close()
        await self.request.close()
        return await super().close()


def load_cogs(bot: Hiyobot):
    extensions = list(
        map(
            lambda path: path.replace("./", "")
            .replace(".py", "")
            .replace("\\", ".")
            .replace("/", "."),
            filter(lambda path: "__" not in path, glob("./hiyobot/cogs/*/*")),
        )
    )
    extensions.append("jishaku")
    failed_list: list[Any] = []

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)
            failed_list.append(extension)

    return failed_list


def run(token: Optional[str]):
    if not token:
        raise ValueError("No token provided")
    intents = Intents.default()
    bot = Hiyobot(command_prefix="&", intents=intents)
    load_cogs(bot)
    # sentry_sdk.init(getenv("SENTRY_DSN"), release=hiyobot.__version__)
    bot.run(token)
