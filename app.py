import os
import uuid
import streamlit as st

from src.pdf_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store, search_similar_chunks
from src.rag_chain import answer_question


UPLOAD_DIR = "data/uploaded_pdfs"


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []


def save_uploaded_file(uploaded_file):
    upload_folder = os.path.join(
        UPLOAD_DIR,
        st.session_state.session_id
    )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF RAG Chatbot")
st.write("Upload a PDF and ask questions from it.")

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")

    file_path = save_uploaded_file(uploaded_file)

    documents = load_pdf(file_path)
    st.write(f"Total pages loaded: {len(documents)}")

    chunks = split_documents(documents)
    st.write(f"Total chunks created: {len(chunks)}")

    with st.spinner("Creating embeddings and FAISS vector store..."):
        embedding_model = get_embedding_model()
        vector_store = create_vector_store(chunks, embedding_model)

    st.session_state.vector_store = vector_store
    st.session_state.chunks = chunks

    st.success("PDF processed successfully!")

st.divider()

st.subheader("Ask a question from your PDF")

question = st.text_input("Enter your question")

if question:
    if st.session_state.vector_store is None:
        st.warning("Please upload a PDF first.")
    else:
        with st.spinner("Searching PDF and generating answer..."):
            retrieved_docs = search_similar_chunks(
                vector_store=st.session_state.vector_store,
                query=question,
                k=6
            )

            answer = answer_question(
                question=question,
                retrieved_docs=retrieved_docs
            )

        st.subheader("Answer")
        st.write(answer)

        with st.expander("View retrieved PDF chunks"):
            for i, doc in enumerate(retrieved_docs):
                st.markdown(f"### Chunk {i + 1}")
                st.write(doc.page_content)

                st.write("Metadata:")
                st.json(doc.metadata)