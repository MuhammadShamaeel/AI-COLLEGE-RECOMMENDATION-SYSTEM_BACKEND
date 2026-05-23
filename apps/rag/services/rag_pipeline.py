from apps.rag.services.retrieval_service import retrieve_relevant_chunks
from apps.rag.services.ollama_service import generate_ai_response


# =============================================================================
# Location keywords recognised from the CSV's Location column.
# Add more as your dataset grows.
# =============================================================================
KNOWN_LOCATIONS = [
    "bangalore", "bengaluru",
    "kerala",
    "mangalore",
    "chennai",
    "coimbatore",
    "palakkad",
    "kozhikode",
    "malappuram",
    "ernakulam",
    "kasaragod",
    "idukki",
    "thrissur",
    "kottayam",
    "kollam",
    "trivandrum", "thiruvananthapuram",
]


def _detect_location(question: str):
    """Return the first location keyword found in the question, else None."""
    q = question.lower()
    for loc in KNOWN_LOCATIONS:
        if loc in q:
            return loc.capitalize()
    return None


def ask_college_assistant(question: str) -> str:
    """
    Full RAG pipeline:
      1. Detect location from question (optional)
      2. Retrieve top-k relevant chunks from FAISS
      3. Build a grounded prompt
      4. Generate a response via Ollama

    Fixed bugs vs. original:
    - Key mismatch: chunks use `college_name` / `location`, not `college`
    - If the location filter returns 0 results, retry without the filter
      so the user always gets an answer (the LLM is still told to be honest).
    """

    detected_location = _detect_location(question)

    # =========================================================================
    # Retrieve chunks (with location filter)
    # =========================================================================

    retrieved_chunks = retrieve_relevant_chunks(
        query=question,
        location=detected_location,
        top_k=5,
    )

    # =========================================================================
    # FIX: if location filter returned nothing, retry without it.
    # This prevents the "No relevant information found." dead-end when the
    # location keyword appears in the question but not in the stored chunks
    # (e.g., the user types "kerala" but chunks say "Kozhikode, Kerala").
    # =========================================================================

    if not retrieved_chunks and detected_location:
        print(
            f"[rag_pipeline] No results for location={detected_location!r}. "
            "Retrying without location filter."
        )
        retrieved_chunks = retrieve_relevant_chunks(
            query=question,
            location=None,
            top_k=5,
        )

    if not retrieved_chunks:
        return (
            "I couldn't find relevant college information for your query. "
            "Please try rephrasing or ask about a specific course, college, or location."
        )

    # =========================================================================
    # Build context string
    # =========================================================================

    context_parts = []

    for chunk in retrieved_chunks:

        # FIX: use `college_name` — the key set by csv_loader / text_splitter
        college_name = chunk.get("college_name", "Unknown College")
        location     = chunk.get("location",     "Unknown Location")
        content      = chunk.get("content",      "")

        context_parts.append(
            f"College: {college_name}\n"
            f"Location: {location}\n"
            f"Details:\n{content}\n"
            f"{'=' * 52}"
        )

    context = "\n\n".join(context_parts)

    # =========================================================================
    # Prompt
    # =========================================================================

    prompt = f"""You are CampusIQ, an AI College Recommendation Assistant for students in India.

Answer the student's question using ONLY the college information provided in the CONTEXT section below.

Guidelines:
- Recommend suitable colleges with their locations
- Mention the relevant course and specialisation
- State the total fee clearly (in INR)
- If multiple colleges match, list all of them
- Be concise and helpful
- Do NOT invent or assume any information not present in the context
- If the context does not contain enough information, say:
  "This information is not available in our current database."

---------------- CONTEXT ----------------

{context}

---------------- STUDENT QUESTION ----------------

{question}

---------------- YOUR ANSWER ----------------
"""

    # =========================================================================
    # Generate and return response
    # =========================================================================

    response = generate_ai_response(prompt)
    return response