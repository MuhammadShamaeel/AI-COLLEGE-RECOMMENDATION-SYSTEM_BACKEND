from apps.rag.services.retrieval_service import retrieve_relevant_chunks
from apps.rag.services.ollama_service import generate_ai_response


def ask_college_assistant(question):

    # ======================================
    # Auto Detect Location From Question
    # ======================================

    detected_location = None

    locations = [
        "bangalore",
        "kerala",
        "mangalore",
        "chennai",
        "coimbatore"
    ]

    for loc in locations:
        if loc.lower() in question.lower():
            detected_location = loc.upper()
            break

    # ======================================
    # Retrieve Relevant Chunks
    # ======================================

    retrieved_chunks = retrieve_relevant_chunks(
        query=question,
        location=detected_location,
        top_k=5
    )

    if not retrieved_chunks:
        return "No relevant information found."

    # ======================================
    # Build Context
    # ======================================

    context = ""

    for chunk in retrieved_chunks:

        college_name = chunk.get("college_name", "Unknown College")
        location = chunk.get("location", "Unknown Location")
        content = chunk.get("content", "")

        context += f"""
College: {college_name}
Location: {location}

Content:
{content}

====================================================
"""

    # ======================================
    # Final Prompt
    # ======================================

    prompt = f"""
You are an AI College Recommendation Assistant.

Your job is to answer student questions ONLY using the provided college brochure information.

Rules:
- Recommend suitable colleges
- Mention courses
- Mention fees if available
- Give detailed helpful answers
- Do NOT generate fake information
- Use ONLY the brochure context

If information is unavailable, say:
"Information not available in brochures."

---------------- CONTEXT ----------------

{context}

---------------- QUESTION ----------------

{question}

---------------- ANSWER ----------------
"""

    # ======================================
    # Generate AI Response
    # ======================================

    response = generate_ai_response(prompt)

    return response