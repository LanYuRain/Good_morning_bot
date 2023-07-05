#前置設定
import discord, json, os
from discord.ext import commands

with open(file="setting.json", mode = "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)#讀取json檔案

intents = discord.Intents.all() #必要設定
bot = commands.Bot(command_prefix="^", intents = intents) #指令前綴是^

#主程式

@bot.event
async def on_ready(): #機器人啟動
    await load_extension()
    print(">>Bot is online<<")

#讀取Cog
async def load_extension():
    for filename in os.listdir("./cmds"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cmds.{filename[:-3]}")

#執行主程式
if __name__ == "__main__":
    bot.run(jdata["TOKEN"])