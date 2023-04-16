import discord
from discord.ext import commands

class dm_basic(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print('dm_basic started!')

	@commands.Cog.listener()
	async def on_message(self, msg):
		if (msg.channel.type != discord.ChannelType.private) | msg.author.bot: return
		await msg.channel.send(f"У вас хороший вкус! Вы, как и я, являетесь участником на серверах: {', '.join([x.name for x in msg.author.mutual_guilds])} :smile:")

async def setup(bot):
	await bot.add_cog(dm_basic(bot))
