from sentence_transformers import SentenceTransformer
import numpy as np


# Load pretrained embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embeddings(chunks):
    """
    Convert text chunks into embeddings
    """

    texts = []

    for chunk in chunks:

        texts.append(
            chunk["content"]
        )

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True
    )

    return np.array(
        embeddings,
        dtype="float32"
    )