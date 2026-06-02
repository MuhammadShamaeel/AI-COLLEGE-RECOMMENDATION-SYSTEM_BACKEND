import faiss
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent.parent
VECTOR_DB_PATH = BACKEND_DIR / "vector_db"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
MAX_L2_DISTANCE = 1.5


def load_vector_store():
    index_path = VECTOR_DB_PATH / "college_index.faiss"
    chunks_path = VECTOR_DB_PATH / "chunks.pkl"

    if not index_path.exists() or not chunks_path.exists():
        print(f"Vector DB not found at {VECTOR_DB_PATH}")
        return None, None

    index = faiss.read_index(str(index_path))
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def retrieve_relevant_chunks(query, state=None, top_k=8):
    """Retrieve relevant chunks based on query and state filter."""
    
    index, chunks = load_vector_store()
    
    if index is None or chunks is None:
        return []

    # Embed query
    query_embedding = np.array(model.encode([query]), dtype="float32")
    
    # Search for more candidates
    search_k = top_k * 3
    distances, indices = index.search(query_embedding, search_k)

    retrieved_chunks = []
    seen_colleges = set()
    
    for rank, idx in enumerate(indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue

        distance = float(distances[0][rank])

        if distance > MAX_L2_DISTANCE:
            continue

        chunk = chunks[idx]
        college_name = chunk.get("college_name", "")

        # Apply state filter
        if state:
            chunk_state = str(chunk.get("state", "")).strip().lower()
            query_state = str(state).strip().lower()
            if query_state not in chunk_state:
                continue

        # Avoid duplicate colleges
        if college_name in seen_colleges:
            continue
        seen_colleges.add(college_name)

        retrieved_chunks.append(chunk)

        if len(retrieved_chunks) >= top_k:
            break

    print(f"[RAG] Found {len(retrieved_chunks)} colleges for '{query}'")
    return retrieved_chunks