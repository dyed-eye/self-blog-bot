import discord
from discord.ext import commands
import os, asyncio, json, sqlite3
import buttons, server


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot("~", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot started as {bot.user}')
        
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
        
@bot.command()
@commands.is_owner()
async def sql(ctx):
    req = ctx.message.content[4:]
    if len(req) == 0:
        return        
    conn = sqlite3.connect("database.db", timeout=20)
    db = conn.cursor()
    try:
        res = db.execute(req[1:]).fetchall()
        await ctx.author.send(res)
    except Exception as e:
        await ctx.author.send(e)
    await ctx.message.delete()
    conn.commit()
    db.close()
    conn.close()

async def load():
	for filename in os.listdir("./cogs"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
	async with bot:
		with open('config.txt', 'r') as f:
			token = f.read()
		await load()
		await bot.start(token)

asyncio.run(main())
