from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    Split each document's content into overlapping chunks for FAISS indexing.

    FIX: chunk_size raised from 500 → 800.
    Each CSV row produces ~200-350 chars of content text.
    A chunk_size of 500 was splitting mid-record on rows with long Notes,
    causing the LLM to receive incomplete fee / course information.
    800 comfortably fits 2-3 full records per chunk while the 150-char
    overlap preserves context across chunk boundaries.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""],
    )

    final_chunks = []

    for doc in documents:

        chunks = text_splitter.split_text(doc["content"])

        for chunk in chunks:

            final_chunks.append(
                {
                    "college_name": doc["college_name"],
                    "location":     doc["location"],
                    "state":        doc.get("state", ""),
                    "content":      chunk,
                }
            )

    print(f"Total chunks created: {len(final_chunks)}")
    return final_chunks