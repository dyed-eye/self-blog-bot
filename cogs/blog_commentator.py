from discord.ext import commands
import server


class blog_commentator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('blog_commentator started!')
        
    @commands.Cog.listener()
    async def on_message(self, message):
        guild = await server.get_data()
        if (message.channel.category_id == guild['blogs']) & (len(message.content) > 0):
            try:
                await message.create_thread(name=message.content[:95], reason="Комментарии")
            except Exception as e:
                print(f'Creating thread problem: {e}')
        
async def setup(bot):
    await bot.add_cog(blog_commentator(bot))
    