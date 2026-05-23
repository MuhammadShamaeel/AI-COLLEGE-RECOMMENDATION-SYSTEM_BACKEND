import faiss
import pickle
import numpy as np
from pathlib import Path


VECTOR_DB_PATH = Path("vector_db")

VECTOR_DB_PATH.mkdir(exist_ok=True)


def save_to_faiss(chunks, embeddings):

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(
        index,
        str(VECTOR_DB_PATH / "college_index.faiss")
    )

    with open(VECTOR_DB_PATH / "chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)