import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer


# Load embedding model
embedding_model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

VECTOR_DB_PATH = "vector_db"


def retrieve_relevant_chunks(
    query,
    top_k=5
):

    # Load FAISS index
    index = faiss.read_index(
        f"{VECTOR_DB_PATH}/college_index.faiss"
    )

    # Load metadata
    with open(
        f"{VECTOR_DB_PATH}/chunks.pkl",
        "rb"
    ) as f:

        chunks = pickle.load(f)

    # Convert query to embedding
    query_embedding = embedding_model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    # Search similar chunks
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        results.append(chunks[idx])

    return results