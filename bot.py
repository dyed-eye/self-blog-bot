import discord
from discord.ext import commands
import os, asyncio, json
import buttons, server


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot("~", intents=intents)

async def make_buttons_work(bot):
    data = await server.get_data()
    channel = bot.get_channel(data['channel_start'])
    message = await channel.fetch_message(data["rules_message"])
    #await message.edit(view=buttons.button_to_start())

@bot.event
async def on_ready():
    print(f'Bot started as {bot.user}')
    try:
        await make_buttons_work(bot)
        print(f'Buttons are working!')
    except Exception:
        raise Exception('Something went wrong activating the buttons')
        
@bot.event
async def on_interaction(int: discord.Interaction):
    ...
    #print(int.data)
    
@bot.command(pass_context=True)
@commands.is_owner()
async def update_tree(ctx):
    res = await bot.tree.sync()
    print(res)
    await ctx.message.delete()
    print('Tree has been updated successfully!')
    
@bot.command(pass_context=True)
@commands.is_owner()
async def get_data(ctx):
    res = await server.get_data()
    await ctx.message.delete()
    await ctx.author.send(json.dumps(res))

async def load():
	for filename in os.listdir("./cogs"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
	async with bot:
		with open('config0.txt', 'r') as f:
			token = f.read()
		await load()
		await bot.start(token)

asyncio.run(main())
