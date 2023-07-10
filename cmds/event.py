import discord, json
from discord.ext import commands
from core.classes import Cog_extension

with open(file="./JSONFiles/setting.json",mode="r",encoding="utf8") as jfile:
    jdata = json.load(jfile)

class Event(Cog_extension):
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(jdata["member_join"])
        await channel.send(f"{member.mention}")

async def setup(bot):
    await bot.add_cog(Event(bot))