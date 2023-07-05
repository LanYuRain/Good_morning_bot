import discord
from discord.ext import commands
from core.classes import Cog_extension

class Main(Cog_extension):
    @commands.command()
    async def test(self,ctx, *,msg):
        await ctx.send(f"Testing {msg}")

async def setup(bot):
    await bot.add_cog(Main(bot))