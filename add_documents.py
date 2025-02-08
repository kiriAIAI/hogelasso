import chromadb
import google.generativeai as genai
import time

import ChatbotPy

# APIキー設定
genai.configure(api_key=ChatbotPy.APIKEY)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"persist_embeddings": True}  # 埋め込みを保存
)


def embed_text(text):
    """Gemini API を使用してテキストをベクトル化する"""
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return response['embedding']



# 初期の構築用
def aaa():
    documents = [
    "FlaskはPythonの軽量Webフレームワークです。",
    "GeminiはGoogleの生成AIモデルです。",
    "RAGは情報検索と生成AIを組み合わせた技術です。",
    ] 
    TTdocuments = [
    "パスワードの再設定は、トップページのアカウントアイコンから「パスワードを忘れた方はこちら」で可能。",
    "会員登録（サインアップ）は、トップページのアカウントアイコンから「初めての方はこちら」で可能。",
    "商品の返品は不可。",
    "支払い方法は、JCB・Visa・Mastercard・Apple Pay・Google Pay に対応。",
    "送料は無料。",
    "購入履歴（注文履歴）は、購入履歴アイコンから確認可能。",
    "オフライン保存は非対応。",
    "ポイントを貯めると記事を読める。",
    "かきっこは基本無料。記事購入は課金の可能性あり。",
    "ログアウトはログインアイコンから可能。",
    "カート内アイテムの削除は、ショッピングカート画面のゴミ箱アイコンから可能。",
    "ポイントは、ショッピングカート画面で入力して使用。",
    "投稿（出品）は、投稿アイコン（プラスマーク）から可能。",
    ]
    
    # ドキュメントを追加 
    for i, doc in enumerate(documents):
        doc_embedding = embed_text(doc)
        collection.add(ids=[str(i)], embeddings=[doc_embedding], documents=[doc])

        print("ドキュメントが登録されました！")
        

def bbb():
    """RAG 用のデータベースを更新"""
    new_documents = [
    # "パスワードの再設定は、トップページのアカウントアイコンから「パスワードを忘れた方はこちら」で可能。",
    "会員登録（サインアップ）は、トップページのアカウントアイコンから「初めての方はこちら」で可能。",
    # "かきっこは基本無料。記事購入は課金の可能性あり。",
    "ログアウトはログインアイコンから可能。",
    "カート内アイテムの削除は、ショッピングカート画面のゴミ箱アイコンから可能。",
    "ポイントは、ショッピングカート画面で入力して使用。",
    "投稿（出品）は、投稿アイコン（プラスマーク）から可能。",
    ]

    # 既存のIDを取得（エラーハンドリングを追加）
    existing_data = collection.get()
    existing_ids = existing_data.get("ids", []) if existing_data else []

    # IDの最大値を取得し、新しい ID を設定
    start_id = max(map(int, existing_ids)) + 1 if existing_ids else 0

    # 新しいドキュメントを追加
    for i, doc in enumerate(new_documents):
        doc_embedding = embed_text(doc)  # Gemini でベクトル化
        if doc_embedding:
            collection.add(ids=[str(start_id + i)], embeddings=[doc_embedding], documents=[doc])
        else:
            print(f"Error: embedding is None for document {i}")

    print("新しいドキュメントが追加されました！")
        
        
def delete():
    all_data = collection.get()  # 現在のデータを取得
    if "ids" in all_data and all_data["ids"]:  # データが存在するか確認
        collection.delete(ids=all_data["ids"])
        print("データベースをリセットしました！")
    else:
        print("データベースには削除するデータがありません。")
        print("データベースをリセットしました！")
        
def kakunin():
    # 登録されているデータを確認
    data = collection.get()
    print(data)

    # 各フィールドを個別に表示
    print("IDリスト:", data["ids"])
    print("文書リスト:", data["documents"])
    print("埋め込みベクトル:", data["embeddings"])

# aaa()
bbb()

# delete()

# print(collection.get())
print(collection.get(include=['embeddings', 'documents', 'metadatas']))
# kakunin()