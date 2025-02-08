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


#------------------------------RAG用データベース----------------------------------------
import chromadb
import google.generativeai as genai

# APIキー設定
genai.configure(api_key=APIKEY)

# ChromaDBのセットアップ
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

def embed_text(text):
    """Gemini APIを使ってテキストをベクトル化"""
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return response["embedding"]


def get_relevant_docs(query, top_k=6):
    """ユーザーのクエリに関連する文書を検索し、類似度スコアを表示"""
    query_embedding = embed_text(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]  # 取得したスコア（距離）

    if not documents:
        return ["関連情報が見つかりませんでした"]

    # Cosine Distance（距離）を Cosine Similarity（類似度）に変換
    similarities = [1 - d for d in distances]  # ChromaDBのデフォルトは距離なので、1 - d で類似度にする

    # スコア付きで文書をリストにまとめる
    ranked_results = [f"スコア: {similarity:.4f} - {doc}" for doc, similarity in zip(documents, similarities)]
    
    return ranked_results



