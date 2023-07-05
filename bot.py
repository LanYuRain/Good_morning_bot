#前置設定
import discord, json
from discord.ext import commands

with open(file="setting.json", mode = "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)#讀取json檔案裡的TOKEN

intents = discord.Intents.all() #必要設定
bot = commands.Bot(commands_prefix="^", intents = intents) #指令前綴是^

#主程式

@bot.event
async def on_ready(): #機器人啟動提示
    print(">>Bot is online<<")


#執行主程式
if __name__ == "__main__":
    bot.run(jdata["TOKEN"])