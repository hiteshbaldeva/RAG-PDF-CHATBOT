from langchain_community.vectorstores import FAISS


def create_vector_store(chunks, embedding_model):
    """
    Creates FAISS vector store from text chunks.
    """

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    return vector_store


def search_similar_chunks(vector_store, query: str, k: int = 3):
    """
    Searches top k similar chunks for the user query.
    """

    results = vector_store.similarity_search(
        query=query,
        k=k
    )

    return results