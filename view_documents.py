import chromadb

# ChromaDBのセットアップ
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

def view_documents():
    """ ChromaDBに登録されているドキュメントを表示 """
    results = collection.get()  # 全てのデータを取得

    for doc_id, doc_text in zip(results["ids"], results["documents"]):
        print(f"ID: {doc_id} - 内容: {doc_text}")

if __name__ == "__main__":
    view_documents()