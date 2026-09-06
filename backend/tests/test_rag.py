from app import rag_service


def test_chunk_text_splits_documents():
    chunks = rag_service.chunk_text(
        "one two three four five",
        chunk_size=3,
        overlap=1
    )

    assert chunks == [
        "one two three",
        "three four five"
    ]


def test_index_knowledge_base(monkeypatch):
    documents = [
        {
            "id": "medical-0",
            "text": "Hemoglobin carries oxygen.",
            "source": "medical_basics.txt"
        },
        {
            "id": "medical-1",
            "text": "White blood cells support immunity.",
            "source": "medical_basics.txt"
        }
    ]
    upserted = {}

    class Embeddings:
        def tolist(self):
            return [[0.1, 0.2], [0.3, 0.4]]

    monkeypatch.setattr(
        rag_service,
        "load_knowledge_base",
        lambda: documents
    )
    monkeypatch.setattr(
        rag_service.embedding_model,
        "encode",
        lambda texts: Embeddings()
    )
    monkeypatch.setattr(
        rag_service.collection,
        "upsert",
        lambda **kwargs: upserted.update(kwargs)
    )

    count = rag_service.index_knowledge_base()

    assert count == 2
    assert upserted["ids"] == ["medical-0", "medical-1"]
    assert upserted["documents"] == [
        "Hemoglobin carries oxygen.",
        "White blood cells support immunity."
    ]