import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer


# =============================================================================
# Embedding model (loaded once at module import to avoid repeated disk reads)
# =============================================================================

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# =============================================================================
# L2 distance threshold
# =============================================================================
# FAISS IndexFlatL2 returns squared-Euclidean distances.
# Embeddings from all-MiniLM-L6-v2 are normalised to unit length, so
# distances lie in [0, 4].  A chunk with distance > 1.5 is semantically
# unrelated to the query and should be discarded.
MAX_L2_DISTANCE = 1.5


def retrieve_relevant_chunks(query, location=None, top_k=5):
    """
    Embed *query*, search FAISS for the nearest chunks, apply an optional
    location filter, and return the best matches.

    Fixed bugs vs. original:
    1. Indentation error in the location-filter block caused the inner `if`
       check to execute even when `location=None`, silently dropping every
       chunk that didn't match the empty string comparison.
    2. Dict key mismatch: chunks are stored as `college_name` / `location`
       but the original code read them as `college` / `location` — the
       wrong key returned None, so the context sent to Ollama was full of
       "Unknown College" placeholders instead of real names.
    3. No distance threshold: FAISS always returns `top_k` results even
       when none of them are relevant. Added MAX_L2_DISTANCE guard.
    4. Location matching was case-sensitive. Now both sides are lowercased.
    """

    # =========================================================================
    # Load FAISS index and chunk store
    # =========================================================================

    index = faiss.read_index("vector_db/college_index.faiss")

    with open("vector_db/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    # =========================================================================
    # Embed query and search
    # =========================================================================

    query_embedding = np.array(
        model.encode([query]), dtype="float32"
    )

    # Fetch more candidates than needed so the location filter has room
    search_k = top_k * 4 if location else top_k
    distances, indices = index.search(query_embedding, search_k)

    # =========================================================================
    # Collect results, applying distance threshold and optional location filter
    # =========================================================================

    retrieved_chunks = []

    for rank, idx in enumerate(indices[0]):

        if idx < 0 or idx >= len(chunks):
            # FAISS returns -1 when the index has fewer items than search_k
            continue

        distance = float(distances[0][rank])

        # FIX 3: skip chunks that are too far from the query
        if distance > MAX_L2_DISTANCE:
            continue

        chunk = chunks[idx]

        # FIX 1 + FIX 4: location filter with correct indentation and
        #                 case-insensitive comparison.
        if location:
            chunk_location = str(chunk.get("location", "")).strip().lower()
            query_location = str(location).strip().lower()

            # Accept the chunk if either string contains the other —
            # e.g. "bangalore" matches "kengeri, bengaluru" and vice-versa.
            if (
                query_location not in chunk_location
                and chunk_location not in query_location
            ):
                continue

        retrieved_chunks.append(chunk)

        if len(retrieved_chunks) >= top_k:
            break

    # =========================================================================
    # Debug output (printed to Django console / logs)
    # =========================================================================

    print(f"\nQuery: {query!r}")
    print(f"Location filter: {location!r}")
    print(f"Retrieved {len(retrieved_chunks)} chunk(s):\n")

    for chunk in retrieved_chunks:
        print("=" * 50)
        # FIX 2: use the correct key `college_name` (not `college`)
        print(f"College:  {chunk.get('college_name', 'N/A')}")
        print(f"Location: {chunk.get('location', 'N/A')}")
        print(f"Content preview: {chunk.get('content', '')[:200]}")
        print()

    return retrieved_chunks