from discord import Embed, Colour, ui, ButtonStyle

class ItemPaginationView(ui.View):
    def __init__(self, ctx, data):
        super().__init__()
        self.ctx = ctx
        self.data = data
        self.current_page = 0

    @ui.button(label="Previous", style=ButtonStyle.primary, custom_id="previous")
    async def previous_button(self, button, interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.get_embed())

    @ui.button(label="Next", style=ButtonStyle.primary, custom_id="next")
    async def next_button(self, button, interaction):
        if self.current_page < len(self.data) // 5:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.get_embed())

    def get_embed(self):
        embed = Embed(title=f":mag: Multiple results", color=Colour.blue())
        for item in self.data[self.current_page*5:(self.current_page+1)*5]:
            value = f":id: ID: {item.id}\n:moneybag: Price: {item.price if item.price not in ['0', 0] else 'N/A'}\n:arrows_counterclockwise: Update: {item.update if item.update not in ['0', 0] else 'N/A'}"
            embed.add_field(name=f"__{item.name}__", value=value, inline=False)
        return embed