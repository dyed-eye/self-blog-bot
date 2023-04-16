import discord
from discord.ext import commands
from datetime import datetime
#from greetings import Greetings


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot("~", intents=intents)
owner = 478621188860411904

@bot.event
async def on_ready():
	# await bot.add_cog(Greetings(bot))
	print(f'Bot started as {bot.user}')

@bot.event
async def on_member_join(member):
	now = datetime.now().strftime("%H:%M:%S")
	print(now)
	with open("gays.txt", "a") as f:
		f.write(f"{member.id} {now}\n")

@bot.command()
async def gays(ctx):
	if ctx.author.id != owner:
		return
	with open("gays.txt", "r") as f:
		await ctx.send(len(f.readlines()))

token = ''
with open('config.txt', 'r') as f:
	token = f.read()
bot.run(token)
