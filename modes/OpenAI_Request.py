import openai, json

#方法回傳值為陣列，建議間結果存到變數再輸出，重複相同請求可能會有意料之外的結果。
def AIChat(user_name,user_id,user_msg):
    with open(file="GPT_APIdata.json",mode="r",encoding="utf8") as apifile:#GPT_APIdata.json讀取api檔案
        data = json.load(apifile)
    with open(file="context.json",mode="r",encoding="utf8") as textfile:#context.json讀取對話紀錄
        context = json.load(textfile)

    openai.api_key = data["apikey"]

    #使用者訊息處理
    input_msg = {"role": "user", "content": ""}
    input_msg["role"] = f"user(Name:{user_name},ID{user_id}.)"
    input_msg["content"] = user_msg

    context.append(input_msg)

    #GPT請求
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=context #List內讀取JSON儲存上下文
    )

    #儲存對話紀錄
    context.append(completion['choices'][0]['message'])
    
    with open(file="context.json",mode="w",encoding="utf8") as textfile:
        json.dump(context, textfile, indent = 4)
    
    #回傳訊息
    result = {
        "content" : str(completion['choices'][0]['message']["content"]),
        "finish_reason" : str({completion['choices'][0]['finish_reason']})[2:-2]
    }
    return result

if __name__ == "__main__":
    while True:
        user_name = "user1"
        user_id = "001"
        user_msg = str(input("> "))
        if user_msg == "/cancel":
            break
        output = AIChat(user_name=user_name,user_id=user_id,user_msg=user_msg)
        print(output["content"])
        print("Fisish reason: ", output["finish_reason"],sep="")