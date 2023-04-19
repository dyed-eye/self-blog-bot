from discord import ui, ButtonStyle, Interaction
from discord.ext import commands


#all button actions are in a distinct cog

class button_to_start(ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        
    @ui.button(style=ButtonStyle.green, label="Создать блог", custom_id="create_blog")
    async def create_blog(self, interaction: Interaction, button: ui.Button):
        ...
        
    @ui.button(style=ButtonStyle.gray, label="Редактировать блог", custom_id="edit_blog")
    async def edit_blog(self, interaction: Interaction, button: ui.Button):
        ...

class buttons_to_approve(ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        
    @ui.button(style=ButtonStyle.green, label="Одобрить", emoji='✔', custom_id="approve")
    async def approve(self, interaction: Interaction, button: ui.Button):
        ...
        
    @ui.button(style=ButtonStyle.red, label="Отклонить", emoji='🚫', custom_id="reject")
    async def reject(self, interaction: Interaction, button: ui.Button):
        ...

class buttons_to_follow(ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        
    @ui.button(style=ButtonStyle.green, label="Подписаться", custom_id="follow")
    async def follow(self, interaction: Interaction, button: ui.Button):
        ...
        
    @ui.button(style=ButtonStyle.red, label="Отписаться", custom_id="unfollow")
    async def unfollow(self, interaction: Interaction, button: ui.Button):
        ...
