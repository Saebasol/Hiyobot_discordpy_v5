# pyright: strict

import re
from typing import Iterable

from aiohttp.client import ClientSession
from discord import Embed
from mintchoco.client import Client
from mintchoco.model import HeliotropeInfo, Tag, HeliotropeImages


class MintChoco(Client):
    client_session: ClientSession

    def get_image_url(self, url: str):
        url_parse_regex = re.compile(
            r"//(..?)(\.hitomi\.la|\.pximg\.net)/(.+?)/(.+)"
        )
        parsed_url: list[str] = url_parse_regex.findall(url)[0]

        prefix = parsed_url[0]
        main_url = parsed_url[1].replace(".", "_")
        type_ = parsed_url[2]
        image = parsed_url[3].replace("/", "_")
        return f"{self.API_URL}/api/proxy/{prefix}_{type_}{main_url}_{image}"

    @staticmethod
    def parse_value_url(value_url_list: Iterable[Tag]):
        if value_url_list:
            return [
                f"[{value_url_dict.value}](https://hitomi.la{value_url_dict.url})"
                for value_url_dict in value_url_list
            ]

        return ["없음"]

    async def close(self):
        await self.client_session.close()

    def make_embed_with_info(self, info: HeliotropeInfo):
        tags_join = (
            ", ".join(self.parse_value_url(info.tags))
                .replace("♀", "\\♀")
                .replace("♂", "\\♂")
        )

        embed = Embed(
            title=info.title,
            description=f"[{info.language.value}]({info.language.url})",
            url=f"https://hitomi.la/galleries/{info.index}.html",
        )

        embed.set_thumbnail(url=self.get_image_url(info.thumbnail))

        embed.add_field(
            name="번호",
            value=f"[{info.index}](https://hitomi.la/reader/{info.index}.html)",
            inline=False,
        )

        embed.add_field(
            name="타입",
            value=f"[{info.type.value}]({info.type.url})",
            inline=False,
        )

        embed.add_field(
            name="작가", value=",".join(self.parse_value_url(info.artist)), inline=False
        )

        embed.add_field(
            name="그룹", value=",".join(self.parse_value_url(info.group)), inline=False
        )

        embed.add_field(
            name="원작", value=",".join(self.parse_value_url(info.series)), inline=False
        )

        embed.add_field(
            name="캐릭터",
            value=",".join(self.parse_value_url(info.characters)),
            inline=False,
        )

        embed.add_field(
            name="태그",
            value=tags_join if len(tags_join) <= 1024 else "표시하기에는 너무 길어요.",
            inline=False,
        )

        return embed

    def make_viewer_embed(self, img_list: HeliotropeImages, total: int) -> list[Embed]:
        embeds = []
        num = 0

        for file_info in img_list.files:
            num += 1
            embeds.append(
                Embed()
                .set_image(url=f"{self.API_URL}/api/proxy/{file_info.url}")
                .set_footer(text=f"{num}/{total} 페이지")
            )

        return embeds

    async def gallery_info(self, index: int):
        search_info = await self.info(index)

        return (
            self.make_embed_with_info(search_info)
            if search_info.status == 200 else
            None
        )

    async def gallery_search(self, query: list[str]):
        search_info = await self.search(query)

        return (
            [self.make_embed_with_info(result) for result in search_info.result]
            if search_info.status == 200 else
            None
        )

    async def gallery_list(self, number: int):
        search_info = await self.list(number)

        return (
            [self.make_embed_with_info(result) for result in search_info.list]
            if search_info.status == 200 else
            None
        )

    async def gallery_viewer(self, index: int):
        search_info = await self.galleryinfo(index)

        return (
            self.make_viewer_embed(await self.images(index), len(list(search_info.files)))
            if search_info.status == 200 else
            None
        )
