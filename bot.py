#前置設定
import discord, json, os
from discord.ext import commands

with open(file="./JSONFiles/setting.json", mode = "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)#讀取json檔案

intents = discord.Intents.all() #必要設定
bot = commands.Bot(command_prefix="^", intents = intents) #指令前綴是^

bot.heartbeat_timeout = 120

#啟動事件

@bot.event
async def on_ready(): #機器人啟動
    await load_extension()
    print(">>Bot is online<<")

#Cog
@bot.command() #加載Cog
async def load(ctx, extension): #放置extension參數，作為指令的參數, ex. load <參數>
    try:
        await bot.load_extension(f"cmds.{extension}")
        await ctx.send(f"Loaded {extension} done.")
    except discord.ext.commands.ExtensionNotFound:
        print(f"User inputted a nonexistent extension: {extension}.")
        await ctx.send(f"{extension} is not exist.")

@bot.command() #卸載Cog
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f"cmds.{extension}")
        await ctx.send(f"Unloaded {extension} done.")
    except discord.ext.commands.ExtensionNotFound:
        print(f"User inputted a nonexistent extension: {extension}.")
        await ctx.send(f"{extension} is not exist.")

@bot.command() #重載Cog
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f"cmds.{extension}")
        await ctx.send(f"Reloaded {extension} done.")
    except discord.ext.commands.ExtensionNotFound:
        print(f"User inputted a nonexistent extension: {extension}.")
        await ctx.send(f"{extension} is not exist.")

async def load_extension():#讀取Cog
    for filename in os.listdir("./cmds"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cmds.{filename[:-3]}")

#執行主程式
if __name__ == "__main__":
    bot.run(jdata["TOKEN"])