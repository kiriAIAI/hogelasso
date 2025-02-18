import google.generativeai as genai
import chromadb
from sentence_transformers import SentenceTransformer


API_KEY = "AIzaSyAWTBtp9Nx5ZI66LL0daEU57DLQgyCoI3U"
MODEL_NAME = "gemini-2.0-flash"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


def text_summary(text):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
        prompt = f"次の内容を基に、物語の冒頭20%を使用して要約し、読者の興味を引く書籍紹介文を生成。長さは約80文字。{text}"
        response = model.generate_content(prompt).text
    except:
        response = ""
    return response

#-------------------------------------チャットボット-------------------------------------------
# ベクトル検索に渡す用
def vectorSearchFunction(text):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
        prompt = f"以下のテキストから冗長な表現や曖昧な語句を削除した自然な日本語に変換してください。出力は変換したテキストのみ。テキスト:{text}"
        response = model.generate_content(prompt)
        return response.text
    except:
        return text

# チャットボット用
def chatbot(prompt, image, history=None):
    try:      
        if history is None:
            chat = model.start_chat(history=[])
        else:
            chat = history
        if image is None:
            response = chat.send_message(prompt)
        else :
            content = []
            content.append(image)
            content.append(prompt)
            response = chat.send_message(content)
        return response.text, chat  # 応答と更新された履歴を返す
    
    except:
        response = "エラーが発生しました。"
        chat = model.start_chat(history=[])
        return response,chat



#------------------------------RAG用検索----------------------------------------

# モデルの遅延ロード
RAG_model = None  

# ChromaDBのセットアップ
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("faq_collection")



def search_faq(user_query):
    try:
        global RAG_model
        if RAG_model is None:
            RAG_model = SentenceTransformer("all-MiniLM-L6-v2")
        user_embedding = RAG_model.encode(user_query).tolist()  # ユーザー入力をベクトル化
        results = collection.query(
            query_embeddings=[user_embedding],
            n_results=2  # 最も近いものを2つ取得
        )
        if results["ids"][0]:  # 一致するデータがあれば表示
            return f'{results["metadatas"][0][0]["A"]} + {results["metadatas"][0][1]["A"]}'
        else:
            return "すみません、該当する情報が見つかりませんでした。"
    except:
        return "エラーが発生しました"
    