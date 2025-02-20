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
        prompt = f"以下のテキストから冗長な表現や曖昧な語句を削除した自然な日本語に変換してください。固有名詞はそのまま。出力は変換したテキストのみ。テキスト:{text}"
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
    
    except Exception as e:
        print(f"エラーが発生しました。 : {e}")
        response = "エラーが発生しました。"
        chat = model.start_chat(history=[])
        return response,chat



#------------------------------ベクトル検索----------------------------------------
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
            n_results=30  # 最も近いものを30つ取得
        )
        list = []
        for i in range(30):
            list.append(results["metadatas"][0][i]["A"])
        return list
    except Exception as e:
        print(f"エラーが発生しました。 : {e}")
        return f"エラーが発生しました"
    
# ーーーーーーーーーーーーーーーーーーーーーーキーワード検索ーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
import spacy
from rank_bm25 import BM25Okapi
# spaCyの日本語モデルをロード
nlp = spacy.load("ja_core_news_sm") 

# 形態素解析（spaCyを使用）
def tokenize(text):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_stop and not token.is_punct]

# 最も関連性の高い3つの質問文を取得する関数
def get_top_3_similar_questions(query, vector_search_results):
    # ベクトル検索結果の質問文をトークン化
    tokenized_corpus = [tokenize(q) for q in vector_search_results]

    # BM25モデルを作成
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = tokenize(query)
    bm25_scores = bm25.get_scores(tokenized_query)
    # スコアが高い順にソート
    sorted_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)
    # 上位3つの質問文を抽出（質問文のみ）
    top_3_questions = [vector_search_results[i] for i in sorted_indices[:3]]

    return top_3_questions