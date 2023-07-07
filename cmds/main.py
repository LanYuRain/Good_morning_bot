import discord
from discord.ext import commands
from core.classes import Cog_extension
from modes.OpenAI_Request import AIChat

class Main(Cog_extension):
    @commands.command()
    async def test(self,ctx, *,msg):
        await ctx.send(f"Testing {msg}")
    
    @commands.command()
    async def ai(self,ctx, *,msg):
        user_id = ctx.author.id
        result = AIChat(user_id=user_id,user_msg=msg)

async def setup(bot):
    await bot.add_cog(Main(bot))