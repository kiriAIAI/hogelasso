import chromadb
from sentence_transformers import SentenceTransformer

# モデルのロード
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDBのセットアップ
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("faq_collection")

# 事前に用意したFAQリスト(この形式にしてね)
# faq_list = [
#     ("返品はできますか？", "未使用品であれば30日以内に返品可能です。"),
# ]



def add_database():
    import csv

    faq_list = []
    with open("kakikko学習データ1.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:  # A列とB列が存在する場合のみ
                faq_list.append((row[0], row[1]))
    print(faq_list)
    
    # データをベクトル化し、ChromaDBに追加
    for i, (question, answer) in enumerate(faq_list):
        embedding = model.encode(question).tolist()  # ベクトル化
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            metadatas=[{"question": question, "answer": answer}]
        )
    print("データベースにFAQを登録しました！")
    


#データ登録（追加するときはchromadbを削除してから実行すること）
# add_database()
