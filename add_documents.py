import chromadb
import google.generativeai as genai

import ChatbotPy

# APIキー設定
genai.configure(api_key=ChatbotPy.APIKEY)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")


# 初期の構築用
def aaa():
    documents = [
    "FlaskはPythonの軽量Webフレームワークです。",
    "GeminiはGoogleの生成AIモデルです。",
    "RAGは情報検索と生成AIを組み合わせた技術です。",
    ] 
    # ドキュメントを追加 
    for i, doc in enumerate(documents):
        doc_embedding = ChatbotPy.embed_text(doc)
        collection.add(ids=[str(i)], embeddings=[doc_embedding], documents=[doc])

        print("ドキュメントが登録されました！")
        
def bbb():
    new_documents = [
        "パスワードの再設定はトップページのアカウントアイコンから”パスワードを忘れた方はこちら”からリセットできます。",
        "会員登録（サインアップ）はトップページのアカウントアイコンから”初めての方はこちら”からアカウントを作ることができます。",
        "商品の返品は受け付けておりません",
        "支払い方法はJCB,Visa,Mastarcard,Apple Pay,Google Payが対応しています。",
        "送料は一切かかりません",
        "購入履歴（注文履歴）は購入履歴アイコンから見ることができます",
        "オフライン保存には対応していません。",
        "ポイントをためることで記事を読むことができます",
        "かきっこはすべての機能を無料で使うことができます。記事の購入には課金が必要になる可能性があります",
        "ログアウトはログインアイコンからログアウトできます",
        "カート内のアイテムを削除したい場合ショッピングカート画面にてゴミ箱アイコンから削除することができます",
        "ポイントはショッピングカート画面にて使用したポイントを入力してください",
        "投稿（出品）は投稿アイコン（プラスマーク）からできます",
    ]
    # 既存のIDを取得し、最大値+1を新しいIDとする
    existing_ids = collection.get()["ids"]
    start_id = max(map(int, existing_ids)) + 1 if existing_ids else 0

    # 新しいドキュメントを追加
    for i, doc in enumerate(new_documents):
        doc_embedding = ChatbotPy.embed_text(doc)
        collection.add(ids=[str(start_id + i)], embeddings=[doc_embedding], documents=[doc])

        print("新しいドキュメントが追加されました！")



bbb()