# pyright: strict

from aiohttp.client import ClientSession
from mintchoco.client import Client


class MintChoco(Client):
    client_session: ClientSession

    async def close(self):
        await self.client_session.close()
