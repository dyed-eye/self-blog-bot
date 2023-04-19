import discord
from discord.ext import commands
from asyncio import TimeoutError
import buttons, server


with open('server_id.txt', 'r') as f:
    gid = int(f.read())

class inguild_setup(commands.GroupCog, name="setup"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        print('inguild_setup started!')
        
    def is_guild(interaction: discord.Interaction):
        return interaction.guild.id == gid

    @discord.app_commands.command(description="Информация о командах")
    @discord.app_commands.check(is_guild)
    @discord.app_commands.checks.has_permissions(manage_guild=True)
    async def info(self, interaction: discord.Interaction):
        title = "Информация"
        text = '· **info** - выводит данное сообщение\n· **starter** - устанавливает канал для старта своего блога. Можно также указать название и содержание информационного сообщения, сопровождающего кнопку "Создать свой блог"\n· **moderation** - устанавливает канал, в который будут приходить новые заявки на создание блога от участников сервера\n· **presentation** - устанавливает канал, в который будет выводиться информация об одобренных блогах, чтобы другие участники могли подписаться\n· **default_role** - выбирает роль, которой обладают авторизованные пользователи (необходимо для настройки блогов)'
        await interaction.response.send_message(embed=discord.Embed.from_dict({"title":title, "description":text, "color":int("ac377c",16), "footer":{"text":f"{interaction.user.name}#{interaction.user.discriminator}", "icon_url":interaction.user.avatar.url}}), ephemeral=True)

    @discord.app_commands.command(description="Отправить стартовое сообщение для блогов")
    @discord.app_commands.check(is_guild)
    @discord.app_commands.checks.has_permissions(manage_guild=True)
    async def starter(self, interaction: discord.Interaction, channel: discord.TextChannel, title: str):
        await interaction.response.send_message("Отправьте содержание сообщения", ephemeral=True, delete_after=30)
        def check(m):
            return (m.author.id == interaction.user.id) & (m.channel.id == interaction.channel.id)
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except TimeoutError:
            print('TimeoutError')
        await msg.delete()
        rules_message = await channel.send(
        embed=discord.Embed.from_dict({"title":title,"description":msg.content,"color":int("ac377c",16),"footer":{"text":f"{self.bot.user.name}#{self.bot.user.discriminator}","icon_url":self.bot.user.avatar.url}}), view=buttons.button_to_start(self.bot))
        res1 = await server.set_value("channel_start", channel.id)
        res2 = await server.set_value("rules_message", rules_message.id)

    @discord.app_commands.command(description="Выбрать канал для модерации заявок")
    @discord.app_commands.check(is_guild)
    @discord.app_commands.checks.has_permissions(manage_guild=True)
    async def moderation(self, interaction: discord.Interaction, channel: discord.TextChannel):
        result = await server.set_value("channel_moderation", channel.id)
        if result:
            await interaction.response.send_message("Канал для модерации заявок успешно настроен!", ephemeral=True)
            
    @discord.app_commands.command(description="Выбрать канал для отправки информации о созданных блогах")
    @discord.app_commands.check(is_guild)
    @discord.app_commands.checks.has_permissions(manage_guild=True)
    async def presentation(self, interaction: discord.Interaction, channel: discord.TextChannel):
        result = await server.set_value("channel_presentation", channel.id)
        if result:
            await interaction.response.send_message("Канал для информации о созданных блогах успешно настроен!", ephemeral=True)
            
    @discord.app_commands.command(description="Выбрать роль авторизованных пользователей")
    @discord.app_commands.check(is_guild)
    @discord.app_commands.checks.has_permissions(manage_guild=True)
    async def default_role(self, interaction: discord.Interaction, role: discord.Role):
        result = await server.set_value("default_role", role.id)
        if result:
            await interaction.response.send_message("Роль авторизованных пользователей успешно установлена!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(inguild_setup(bot))
