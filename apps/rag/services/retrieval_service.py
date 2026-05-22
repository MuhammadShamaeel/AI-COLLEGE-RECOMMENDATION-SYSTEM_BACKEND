import os
import pickle
import faiss

from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_relevant_chunks(query, location=None, top_k=5):

    base_path = "vector_db"

    index_path = os.path.join(base_path, "college_index.faiss")
    chunks_path = os.path.join(base_path, "chunks.pkl")

    index = faiss.read_index(index_path)

    with open(chunks_path, "rb") as f:
        stored_data = pickle.load(f)

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = []

    for idx in indices[0]:

        chunk_data = stored_data[idx]

        # LOCATION FILTER
        if location:
            if chunk_data["location"].lower() != location.lower():
                continue

        retrieved_chunks.append(chunk_data)

    return retrieved_chunks