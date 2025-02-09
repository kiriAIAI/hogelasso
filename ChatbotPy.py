from google import genai
import chromadb
from sentence_transformers import SentenceTransformer



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


#------------------------------RAG用検索----------------------------------------

# モデルの遅延ロード
model = None  

# ChromaDBのセットアップ
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("faq_collection")



def search_faq(user_query):
    try:
        if model is None:
            model = SentenceTransformer("all-MiniLM-L6-v2")
        user_embedding = model.encode(user_query).tolist()  # ユーザー入力をベクトル化
        results = collection.query(
            query_embeddings=[user_embedding],
            n_results=2  # 最も近いものを2つ取得
        )
        if results["ids"][0]:  # 一致するデータがあれば表示
            return results["metadatas"][0][0]["answer"] + results["metadatas"][0][1]["answer"]
        else:
            return "すみません、該当する情報が見つかりませんでした。"
    except:
        return "エラーが発生しました"



