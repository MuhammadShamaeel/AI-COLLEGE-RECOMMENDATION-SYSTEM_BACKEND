import faiss
import pickle
import numpy as np
import os


VECTOR_DB_PATH = "vector_db"


def save_to_faiss(chunks, embeddings):

    os.makedirs(
        VECTOR_DB_PATH,
        exist_ok=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(
            embeddings,
            dtype="float32"
        )
    )

    # Save FAISS index
    faiss.write_index(
        index,
        f"{VECTOR_DB_PATH}/college_index.faiss"
    )

    # Save metadata
    with open(
        f"{VECTOR_DB_PATH}/chunks.pkl",
        "wb"
    ) as f:

        pickle.dump(chunks, f)

    print("\nVector DB Saved")