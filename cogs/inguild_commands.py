import discord
from discord.ext import commands

class inguild_commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print('inguild started!')

	@commands.hybrid_group(fallback="info", description="Информация о командах")
	@commands.has_permissions(manage_guild=True)
	async def set(self, ctx):
		title = "Информация"
		text = '**info** - выводит данное сообщение\n**starter** - устанавливает канал для старта своего блога. Можно также указать название и содержание информационного сообщения, сопровождающего кнопку "Создать свой блог"\n**moderation** - устанавливает канал, в который будут приходить новые заявки на создание блога от участников сервера\n**presentation** - устанавливает канал, в который будет выводиться информация об одобренных блогах, чтобы другие участники могли подписаться'
		await ctx.send(embed=discord.Embed.from_dict({"title":title, "description":text, "color":int("ac377c",16), "footer":{"text":f"{ctx.author.name}#{ctx.author.discriminator}", "icon_url":ctx.author.avatar.url}}))

	@set.command(description="Отправить стартовое сообщение для блогов")
	@commands.has_permissions(manage_guild=True)
	async def starter(self, ctx, channel: discord.TextChannel):
		await ctx.send("Success!")

async def setup(bot):
	await bot.add_cog(inguild_commands(bot))
