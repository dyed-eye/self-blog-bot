import discord
from discord.ext import commands
import sqlite3
import buttons, server


class button_actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('button_actions started!')

    async def create_blog(self, interaction:discord.Interaction):
        conn = sqlite3.connect("database.db")
        db = conn.cursor()
        status = db.execute(f'SELECT status FROM applications WHERE author={interaction.user.id} LIMIT 1').fetchall()
        if len(status) > 0:
            await interaction.response.send_message("У вас уже есть блог!", ephemeral=True)
            return
        db.execute(f"INSERT INTO applications VALUES ({interaction.user.id}, 'new', 'title', 'description')")
        await interaction.user.send("Вы подали заявку на создание блога! В ответ на это сообщение напишите его будущее название")
        await interaction.response.send_message("Проверьте личные сообщения!", ephemeral=True)
        def check(m):
            return (m.author.id == interaction.user.id) & (m.channel.type == discord.ChannelType.private)
        title = ''
        while title == '':
            title = await self.bot.wait_for('message', check=check)
            title = title.content
        await interaction.user.send("Теперь придумайте описание")
        description = ''
        while description == '':
            description = await self.bot.wait_for('message', check=check)
            description = description.content
        db.execute("UPDATE applications SET status = 'created', title = ?, description = ? WHERE author = ?", (title, description, interaction.user.id))
        guild = await server.get_data()
        channel = self.bot.get_channel(guild['channel_moderation'])
        await channel.send(embed=discord.Embed.from_dict({"title":"Заявка на создание блога", "description":f"**{title}**\n{description}", "color":int("ac377c",16), "footer":{"text":f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})", "icon_url":interaction.user.avatar.url}}), view=buttons.buttons_to_approve())
        await interaction.user.send("Отлично! Ваша заявка на создание блога уже рассматривается модерацией, ожидайте")
        conn.commit()
        conn.close()

    async def edit_blog(self, interaction:discord.Interaction):
        conn = sqlite3.connect("database.db")
        db = conn.cursor()
        status = db.execute(f'SELECT status FROM applications WHERE author={interaction.user.id} LIMIT 1').fetchall()
        if len(status) == 0:
            await interaction.response.send_message("У вас нет блога!", ephemeral=True)
            return
        elif status != "approved":
            await interaction.response.send_message("Ваш блог находится в процессе создания/модерации!", ephemeral=True)
            return
        await interaction.user.send("Вы подали заявку на редактирование блога! В ответ на это сообщение напишите его новое название")
        await interaction.response.send_message("Проверьте личные сообщения!", ephemeral=True)
        def check(m):
            return (m.author.id == interaction.user.id) & (m.channel.type == discord.ChannelType.private)
        title = ''
        while title == '':
            title = await self.bot.wait_for('message', check=check)
            title = title.content
        await interaction.user.send("Теперь придумайте новое описание")
        description = ''
        while description == '':
            description = await self.bot.wait_for('message', check=check)
            description = description.content
        db.execute("UPDATE applications SET status = 'edited', title = ?, description = ? WHERE author = ?", (title, description, interaction.user.id))
        guild = await server.get_data()
        channel = self.bot.get_channel(guild['channel_moderation'])
        await channel.send(embed=discord.Embed.from_dict({"title":"Заявка на редактирование блога", "description":f"**{title}**\n{description}", "color":int("ac377c",16), "footer":{"text":f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})", "icon_url":interaction.user.avatar.url}}), view=buttons.buttons_to_approve())
        await interaction.user.send("Отлично! Ваша заявка на редактирование блога уже рассматривается модерацией, ожидайте")
        conn.commit()
        conn.close()

    async def approve(self, interaction:discord.Interaction):
        print('yes')
        await interaction.message.delete()
        #await interaction.message.edit(f"Заявка одобрена модератором {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})", view=None)
        print('yes')
        await interaction.response.send_message("Заявка одобрена!", ephemeral=True)
        print('yes')

    async def reject(self, interaction:discord.Interaction):
        await interaction.edit_original_response(f"Заявка отклонена модератором {interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})", view=None)
        await interaction.response.send_message("Заявка отклонена!", ephemeral=True)

    async def follow(self, interaction:discord.Interaction):
        await interaction.response.send_message("Вы подписались!", ephemeral=True)

    async def unfollow(self, interaction:discord.Interaction):
        await interaction.response.send_message("Вы отписались!", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_interaction(self, int: discord.Interaction):
        match int.data['custom_id']:
            case "create_blog":
                await self.create_blog(int)
            case "edit_blog":
                await self.edit_blog(int)
            case "approve":
                await self.approve(int)
            case "reject":
                await self.reject(int)
            case "follow":
                await self.follow(int)
            case "unfollow":
                await self.unfollow(int)
            case _:
                ...

async def setup(bot):
    await bot.add_cog(button_actions(bot))
