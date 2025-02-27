import chromadb, json
from sentence_transformers import SentenceTransformer
# モデルのロード
model = SentenceTransformer("all-MiniLM-L6-v2")


# ChromaDBのセットアップ
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("faq_collection",metadata={"persist_embeddings": True})

# 事前に用意したFAQリスト(この形式にしてね)
# faq_list = [
#     ("返品はできますか？", "未使用品であれば30日以内に返品可能です。"),
# ]



def add_database():
    import csv

    faq_list = []
    with open("チャットボット学習データ\kakikko学習データ_v3(複数パターン).csv", encoding="utf-8") as file:
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
            metadatas=[{"Q": question, "A": answer}]
        )
    print("データベースにFAQを登録しました！")
    


#データ登録（追加するときはchromadbを削除してから実行すること）
add_database()

def jsonex():
    results = collection.get(include=['embeddings', 'documents', 'metadatas'])

    # 必要な情報を JSON 形式で整形
    data_to_export = []
    for i in range(len(results["ids"])):
        data_to_export.append({
            "id": results["ids"][i],
            "embedding": results["embeddings"][i].tolist(),  # ndarray をリストに変換
            "metadata": results["metadatas"][i]
        })

    # JSON ファイルに保存
    with open("チャットボット学習データ/exported_data.json", "w") as f:
        json.dump(data_to_export, f, indent=4)

    print("データのエクスポートが完了しました。")
    
#jsonファイルにエクスポート
jsonex()
