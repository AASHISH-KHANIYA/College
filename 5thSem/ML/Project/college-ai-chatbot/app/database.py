import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="./data/chroma"
)

collection = client.get_or_create_collection(
    name="college_knowledge"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def add_documents(documents):

    if not documents:
        return 0

    texts = [doc["text"] for doc in documents]

    embeddings = embedding_model.encode(
        texts
    ).tolist()

    ids = [
        f"doc_{collection.count() + i}"
        for i in range(len(texts))
    ]

    metadatas = [
        {
            "source": str(doc["source"]),
            "sheet": str(doc["sheet"])
        }
        for doc in documents
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(texts)


def search(query, n_results=5):

    embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=embedding,
        n_results=n_results
    )

    return results["documents"][0]