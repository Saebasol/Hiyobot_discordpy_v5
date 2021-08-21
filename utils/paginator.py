# pyright: strict

from typing import Optional
from discord.enums import ButtonStyle
from discord.interactions import Interaction
from discord.ui.button import button
from discord.ui.view import View
from discord.embeds import Embed


class Paginator(View):
    def __init__(
        self, executor_id: int, embeds: list[Embed], timeout: Optional[float] = 60
    ):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.executor_id = executor_id
        self.index = 0

    @property
    def total(self):
        return len(self.embeds)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if user := interaction.user:
            if user.id == self.executor_id:
                return True

            await interaction.response.send_message(
                "명령어 실행자만 상호작용이 가능합니다.", ephemeral=True
            )

        return False

    @button(label="이전", style=ButtonStyle.green, emoji="◀")
    async def prev_page(self, _, interaction: Interaction):
        self.index -= 1

        if self.index < 0:
            self.index = self.total - 1

        await interaction.response.edit_message(embed=self.embeds[self.index])

    @button(label="다음", style=ButtonStyle.green, emoji="▶️")
    async def next_page(self, _, interaction: Interaction):
        self.index += 1

        if self.index >= self.total:
            self.index = 0

        await interaction.response.edit_message(embed=self.embeds[self.index])

    @button(label="닫기", style=ButtonStyle.danger, emoji="❌")
    async def close(self, _, interaction: Interaction):
        if message := interaction.message:
            self.stop()
            await message.delete()
