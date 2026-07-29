from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embedding_model():
    """
    Creates and returns the embedding model.

    Embeddings convert text into numerical vectors.
    FAISS stores these vectors and searches similar vectors.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embedding_model