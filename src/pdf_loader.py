from langchain_community.document_loaders import PyMuPDFLoader


def load_pdf(file_path: str):
    """
    Loads a PDF file and returns documents page by page.

    Each document contains:
    - page_content: text from that page
    - metadata: page number, source file path, etc.
    """

    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    return documents