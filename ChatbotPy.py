# import google.generativeai as genai
from google import genai

APIKEY = "AIzaSyAWTBtp9Nx5ZI66LL0daEU57DLQgyCoI3U"
geminiModel = "gemini-2.0-flash"

client = genai.Client(api_key=APIKEY)
chat = client.chats.create(model=geminiModel)

def text_summary(text):
    response = client.models.generate_content(
        model=geminiModel,
        contents=["次の内容を基に、物語の冒頭20%を使用して要約し、読者の興味を引く書籍紹介文を生成。長さは約80文字。"+ text])
    return response.text

def textGen(text):
    response = chat.send_message(text)
    print(response.text)
    return response.text

def textImageGen(text,image):
    response = client.models.generate_content(
        model=geminiModel,
        contents=[image, text])
    print(response.text)
    return response.text