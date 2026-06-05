from text_ai.services.rag.embedding_service import get_embedding


def retrieve_context(vector_store, query: str):
    if not query:
        return []
    embedding = get_embedding(query)
    results = vector_store.search(embedding)

    # remove duplicates
    unique_results = []
    seen = set()
    for result in results:
        if result not in seen:
            unique_results.append(result)
            seen.add(result)
    return unique_results
