from app.rag_service import (
    index_knowledge_base,
    build_context
)

count = index_knowledge_base()
print(
    f"Indexed {count} knowledge chunks."
)

query = "What is hemoglobin?"
context = build_context(query)
print("\nRetrieved context:\n")
print(context)