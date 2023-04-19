import discord
from discord.ext import commands
import sqlite3
from datetime import datetime
import buttons, server


class button_actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('button_actions started!')
        
    async def create(self, author, title, description):
        guild = await server.get_data()
        cat = self.bot.get_channel(guild['blogs'])
        default_role = cat.guild.get_role(guild['default_role'])
        user = self.bot.get_user(author)
        channel = await cat.create_text_channel(title, reason="Создание блога", topic=description, overwrites={
            default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, create_private_threads=False, create_public_threads=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, create_private_threads=False, create_public_threads=True)
        })
        channel_presentation = self.bot.get_channel(guild['channel_presentation'])
        presentation = await channel_presentation.send(embed=discord.Embed.from_dict({"title":title, "description":description, "color":int("ac377c",16), "footer":{"text":f"{user.name}#{user.discriminator}", "icon_url":user.avatar.url}}), view=buttons.buttons_to_follow())
        return presentation.id, channel.id
        
    async def edit(self, author, title, description, presentation, blog):
        guild = await server.get_data()
        blog_channel = self.bot.get_channel(blog)
        await blog_channel.edit(name=title, topic=description, reason="Изменение блога")
        user = self.bot.get_user(author)
        channel_presentation = self.bot.get_channel(guild['channel_presentation'])
        presentation_old = await channel_presentation.fetch_message(presentation)
        await presentation_old.delete()
        presentation = await channel_presentation.send(embed=discord.Embed.from_dict({"title":title, "description":description, "color":int("ac377c",16), "footer":{"text":f"{user.name}#{user.discriminator}", "icon_url":user.avatar.url}}), view=buttons.buttons_to_follow())
        return presentation.id

    async def create_blog(self, interaction:discord.Interaction):
        conn = sqlite3.connect("database.db")
        db = conn.cursor()
        status = db.execute(f'SELECT status FROM applications WHERE author={interaction.user.id} LIMIT 1').fetchall()
        if len(status) > 0:
            if status[0] == "rejected":
                blog = db.execute(f'SELECT * FROM blogs WHERE author={interaction.user.id} LIMIT 1').fetchall()
                if len(blog) > 0:
                    await interaction.response.send_message("У вас уже есть блог!", ephemeral=True)
                    return
            else:
                await interaction.response.send_message("У вас уже есть блог!", ephemeral=True)
                return
        db.execute(f"INSERT INTO applications VALUES ({interaction.user.id}, 'new', 'title', 'description', 0)")
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
        guild = await server.get_data()
        channel = self.bot.get_channel(guild['channel_moderation'])
        msg = await channel.send(embed=discord.Embed.from_dict({"title":"Заявка на создание блога", "description":f"**{title}**\n{description}", "color":int("ac377c",16), "footer":{"text":f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})", "icon_url":interaction.user.avatar.url}}), view=buttons.buttons_to_approve())
        db.execute("UPDATE applications SET status = 'created', title = ?, description = ?, moderation = ? WHERE author = ?", (title, description, msg.id, interaction.user.id))
        await interaction.user.send("Отлично! Ваша заявка на создание блога уже рассматривается модерацией, ожидайте")
        conn.commit()
        db.close()
        conn.close()

    async def edit_blog(self, interaction:discord.Interaction):
        conn = sqlite3.connect("database.db")
        db = conn.cursor()
        status = db.execute(f'SELECT status FROM applications WHERE author={interaction.user.id} LIMIT 1').fetchall()
        if len(status) == 0:
            await interaction.response.send_message("У вас нет блога!", ephemeral=True)
            return
        elif status[0] in ['new','created','edited']:
            await interaction.response.send_message("Ваш блог находится в процессе создания/модерации!", ephemeral=True)
            return
        try:
            db.execute(f"UPDATE applications SET status = 'edited' WHERE author={interaction.user.id}")
        except Exception as e:
            print(e)
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
        guild = await server.get_data()
        channel = self.bot.get_channel(guild['channel_moderation'])
        msg = await channel.send(embed=discord.Embed.from_dict({"title":"Заявка на редактирование блога", "description":f"**{title}**\n{description}", "color":int("ac377c",16), "footer":{"text":f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})", "icon_url":interaction.user.avatar.url}}), view=buttons.buttons_to_approve())
        db.execute("UPDATE applications SET status = 'edited', title = ?, description = ?, moderation = ? WHERE author = ?", (title, description, msg.id, interaction.user.id))
        await interaction.user.send("Отлично! Ваша заявка на редактирование блога уже рассматривается модерацией, ожидайте")
        conn.commit()
        db.close()
        conn.close()

    async def approve(self, interaction:discord.Interaction):
        conn = sqlite3.connect("database.db")
        db = conn.cursor()
        try:
            res = db.execute(f"SELECT author, status, title, description FROM applications WHERE moderation = {interaction.message.id}").fetchone()
            author, status, title, description = res
            user = self.bot.get_user(author)
            if status == "created":
                await user.send(f'Поздравляю! Ваша заявка на создание блога "{title}" одобрена')
                presentation, blog = await self.create(author, title, description)
                db.execute(f"INSERT INTO blogs VALUES (?, ?, ?, ?, ?, ?)", (author, title, description, presentation, blog, datetime.today().strftime('%Y-%m-%d')))
            else:
                res = db.execute(f"SELECT presentation, blog FROM blogs WHERE author = {author}").fetchone()
                presentation, blog = res
                await user.send(f'Поздравляю! Ваша заявка на редактирование блога "{title}" одобрена')
                presentation = await self.edit(author, title, description, presentation, blog)
                db.execute(f'UPDATE blogs SET title = ?, description = ?, presentation = ?, date_of_edit = ? WHERE author = ?', (title, description, presentation, datetime.today().strftime('%Y-%m-%d'), author))
            db.execute(f"UPDATE applications SET status = 'approved' WHERE moderation = {interaction.message.id}")
            await interaction.message.edit(content=f"Заявка одобрена модератором <@{interaction.user.id}> ({interaction.user.id})", view=None)
        except Exception as e:
            print(e)
        await interaction.response.send_message("Заявка одобрена!", ephemeral=True)
        conn.commit()
        conn.close()

    async def reject(self, interaction:discord.Interaction):
        conn = sqlite3.connect("database.db")
        db = conn.cursor()
        try:
            res = db.execute(f"SELECT author, status, title, description FROM applications WHERE moderation = {interaction.message.id}").fetchone()
            author, status, title, description = res
            user = self.bot.get_user(author)
            if status == "created":
                await user.send(f'К сожалению, ваша заявка на создание блога "{title}" отклонена')
            else:
                await user.send(f'К сожалению, ваша заявка на редактирование блога "{title}" отклонена')
            db.execute(f"UPDATE applications SET status = 'rejected' WHERE moderation = {interaction.message.id}")
            await interaction.message.edit(content=f"Заявка отклонена модератором <@{interaction.user.id}> ({interaction.user.id})", view=None)
        except Exception as e:
            print(e)
        await interaction.response.send_message("Заявка отклонена!", ephemeral=True)
        conn.commit()
        conn.close()

    async def follow(self, interaction:discord.Interaction):
        try:
            conn = sqlite3.connect("database.db")
            db = conn.cursor()
            blog, _ = db.execute(f"SELECT blog, author FROM blogs WHERE presentation = {interaction.message.id}").fetchone()
            blog_channel = self.bot.get_channel(blog)
            await blog_channel.set_permissions(interaction.user, read_messages=True, send_messages=False)
            await interaction.response.send_message("Вы подписались!", ephemeral=True)
            db.close()
            conn.close()
        except Exception as e:
            print(e)

    async def unfollow(self, interaction:discord.Interaction):
        conn = sqlite3.connect("database.db")
        db = conn.cursor()
        blog, _ = db.execute(f"SELECT blog, author FROM blogs WHERE presentation = {interaction.message.id}").fetchone()
        blog_channel = self.bot.get_channel(blog)
        await blog_channel.set_permissions(interaction.user, read_messages=False)
        await interaction.response.send_message("Вы отписались!", ephemeral=True)
        db.close()
        conn.close()
    
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
