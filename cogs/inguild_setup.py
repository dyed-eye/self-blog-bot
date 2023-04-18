import discord
from discord.ext import commands


class button_to_start(discord.ui.View):
	def __init__(self, *, timeout=None):
		super().__init__(timeout=timeout)
    
	@discord.ui.button(style=discord.ButtonStyle.green, label="Создать блог")
	async def create_blog(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.user.send("Здравствуйте")
		await interaction.response.send_message("Проверьте личные сообщения!", ephemeral=True)

class inguild_setup(commands.GroupCog, name="setup"):
	def __init__(self, bot):
		self.bot = bot
		super().__init__()
		print('inguild_setup started!')

	@discord.app_commands.command(description="Информация о командах")
	@commands.has_permissions(manage_guild=True)
	async def info(self, interaction: discord.Interaction):
		title = "Информация"
		text = '**info** - выводит данное сообщение\n**starter** - устанавливает канал для старта своего блога. Можно также указать название и содержание информационного сообщения, сопровождающего кнопку "Создать свой блог"\n**moderation** - устанавливает канал, в который будут приходить новые заявки на создание блога от участников сервера\n**presentation** - устанавливает канал, в который будет выводиться информация об одобренных блогах, чтобы другие участники могли подписаться'
		await interaction.response.send_message(embed=discord.Embed.from_dict({"title":title, "description":text, "color":int("ac377c",16), "footer":{"text":f"{interaction.user.name}#{interaction.user.discriminator}", "icon_url":interaction.user.avatar.url}}), ephemeral=True)

	@discord.app_commands.command(description="Отправить стартовое сообщение для блогов")
	@commands.has_permissions(manage_guild=True)
	async def starter(self, interaction: discord.Interaction, channel: discord.TextChannel, title: str, description: str):
		await channel.send(
		embed=discord.Embed.from_dict({
        	"title":title,"description":description,"color":int("ac377c",16),"footer":{
        		"text":f"{self.bot.user.name}#{self.bot.user.discriminator}","icon_url":self.bot.user.avatar.url
        	}
        }),
        view=button_to_start()
        )
		await interaction.response.send_message("Success!", ephemeral=True)

async def setup(bot):
	await bot.add_cog(inguild_setup(bot))
