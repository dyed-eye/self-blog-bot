import discord
from discord.ext import commands
import os
import asyncio


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot("~", intents=intents)

@bot.event
async def on_ready():
	# await bot.add_cog(Greetings(bot))
	print(f'Bot started as {bot.user}')
    
@bot.command(pass_context=True)
@commands.is_owner()
async def update_tree(ctx):
    res = await bot.tree.sync()
    print(res)
    await ctx.message.delete()
    print('Tree has been updated successfully!')

async def load():
	for filename in os.listdir("./cogs"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
	async with bot:
		token = ''
		with open('config0.txt', 'r') as f:
			token = f.read()
		await load()
		await bot.start(token)

asyncio.run(main())
