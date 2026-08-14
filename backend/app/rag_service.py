from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

KNOWLEDGE_BASE_DIR = Path("../../knowledge_base")
CHROMA_DIR = Path("../../chroma_db")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = chroma_client.get_or_create_collection(
    name="medical_knowledge"
)

def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def load_knowledge_base():

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):
        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            documents.append({
                "id": f"{file_path.stem}-{index}",
                "text": chunk,
                "source": file_path.name
            })

    return documents

def index_knowledge_base():
    documents = load_knowledge_base()

    if not documents:
        raise ValueError(
            "No knowledge base documents found."
        )

    texts = [
        document["text"]
        for document in documents
    ]

    ids = [
        document["id"]
        for document in documents
    ]

    metadatas = [
        {
            "source": document["source"]
        }
        for document in documents
    ]

    embeddings = embedding_model.encode(
        texts
    ).tolist()

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(documents)

def search_knowledge(
        query: str,
        top_k: int = 3
):
    query_embedding = embedding_model.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    return documents