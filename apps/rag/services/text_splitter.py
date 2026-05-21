from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for doc in documents:

        split_texts = text_splitter.split_text(
            doc["text"]
        )

        for chunk in split_texts:

            chunks.append(
                {
                    "college": doc["college"],
                    "location": doc["location"],
                    "content": chunk
                }
            )

    return chunks