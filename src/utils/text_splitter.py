from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_splitter(chunk_size: int = 500, overlap: int = 100):
    """
    Returns a RecursiveCharacterTextSplitter with recommended settings.
    Splits text into overlapping chunks suitable for embeddings and RAG.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "! ",
            "? ",
            ", ",
            " ",
            ""
        ]
    )
    return splitter
