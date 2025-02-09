import chromadb , json

# ChromaDBのセットアップ
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("faq_collection")


# JSON からデータを復元
with open("exported_data.json", "r") as f:
    data = json.load(f)
    for item in data:
        collection.delete(ids=[item["id"]])  # 既存のデータを削除
        collection.add(
            ids=[item["id"]],
            embeddings=[item["embedding"]],
            metadatas=[item["metadata"]]
        )
        
        
print(collection.get(include=['embeddings', 'documents', 'metadatas']))