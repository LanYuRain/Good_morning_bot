import discord,time,json
from discord.ext import commands
from core.classes import Cog_extension
from modes.OpenAI_Request import AIChat

with open(file="./JSONFiles/context.json",mode="r",encoding="utf8") as textfile:#context.json讀取對話紀錄
        context = json.load(textfile)

class AI(Cog_extension):
    #file_route
    fileName_context = "./JSONFiles/context.json"
    fileName_GPT_APIdata = "./JSONFiles/GPT_APIdata.json"
    fileName_context_default = "./JSONFiles/context_default.json"
    fileName_setting = "./JSONFiles/setting.json"
    #速率與對話限制
    max_context_len = 29 #最大對話紀錄長度
    cmd_cd_time = 30 #指令冷卻時間
    
    @commands.command()
    async def chat(self,ctx, *,msg):
        #讀取json檔案
        with open(file=self.fileName_setting, mode = "r", encoding="utf8") as jfile:#讀取設定檔
            jdata = json.load(jfile)
        with open(file=self.fileName_context,mode="r",encoding="utf8") as textfile:#context.json讀取對話紀錄
            context = json.load(textfile)
        #執行
        
        if ((time.time() - jdata["time"]) >= self.cmd_cd_time) and (len(context) <= self.max_context_len):
            #文件路徑
            user_name = ctx.author#輸入者名稱 
            #API處理
            await ctx.send("> 思考中，請稍後...")
            result = AIChat(fileName_GPT_APIdata=self.fileName_GPT_APIdata,fileName_context=self.fileName_context,user_name=user_name,user_msg=msg)
            await ctx.send(result["content"])
            #回傳例外處理
            if(result["finish_reason"] == "length"):
                await ctx.send("```超出限制，訊息可能不完整。```")
            elif(result["finish_reason"] == "content_filter"):
                await ctx.send("```訊息內容被過濾。```")
            #儲存執行時間
            jdata["time"] = time.time()
            with open(file=self.fileName_setting, mode = "w", encoding="utf8") as jfile:
                json.dump(jdata,jfile,indent=4)
            #對話次數提示
            if len(context) == self.max_context_len:
                #對話紀錄長度限制
                with open(file=self.fileName_context_default,mode="r",encoding="utf8") as textfile:#context.json讀取對話紀錄
                    context_default = json.load(textfile)
                with open(file=self.fileName_context, mode = "w", encoding="utf8") as jfile:
                    json.dump(context_default,jfile,indent=4)
                await ctx.send(f"> ♻️限制♻️ 伺服器對話紀錄已被重置。")
            else:  
                await ctx.send(f"> ♻️限制♻️ 伺服器對話紀錄剩餘`{int(self.max_context_len / 2) - int(len(context) / 2)}`次將被重置。")
        elif (time.time() - jdata["time"]) < self.cmd_cd_time:
            #指令冷卻
            cd = int(time.time() - jdata["time"])
            await ctx.send(f"> ***AI需要冷卻！**共**{self.cmd_cd_time}**秒，剩餘`{self.cmd_cd_time - cd}`秒*")
    @commands.command()
    async def resetAI(self,ctx):
        #reset
        with open(file=self.fileName_context_default,mode="r",encoding="utf8") as textfile:#context.json讀取對話紀錄
            context_default = json.load(textfile)
        with open(file=self.fileName_context, mode = "w", encoding="utf8") as jfile:
            json.dump(context_default,jfile,indent=4)
        await ctx.send(f"> 伺服器對話紀錄已被重置。")

async def setup(bot):
    await bot.add_cog(AI(bot))