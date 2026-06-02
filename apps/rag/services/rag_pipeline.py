from apps.rag.services.retrieval_service import retrieve_relevant_chunks
from apps.rag.services.ollama_service import generate_ai_response


def format_college_info(chunks):
    """Format college information in a clean, readable way."""
    colleges = []
    seen = set()
    
    for chunk in chunks:
        college_name = chunk.get("college_name", "")
        if college_name in seen:
            continue
        seen.add(college_name)
        
        location = chunk.get("location", "Unknown")
        state = chunk.get("state", "Unknown")
        content = chunk.get("content", "")
        
        # Parse content for course and fee
        lines = content.split('\n')
        course = ""
        fee = ""
        
        for line in lines:
            if 'Course' in line or 'Specialization' in line:
                course = line.split(':')[-1].strip() if ':' in line else line
            if 'Fee' in line or 'INR' in line:
                fee = line.split(':')[-1].strip() if ':' in line else line
        
        colleges.append({
            "name": college_name,
            "location": f"{location}, {state}",
            "course": course[:100] if course else "Various Programs",
            "fee": fee if fee else "Contact college"
        })
    
    return colleges


def ask_college_assistant(question: str, context_state: str = None, context_location: str = None) -> str:
    """
    RAG pipeline for college recommendations.
    """
    # Retrieve relevant chunks
    retrieved_chunks = retrieve_relevant_chunks(
        query=question,
        state=context_state,
        top_k=8,
    )

    if not retrieved_chunks:
        return f"I couldn't find any colleges matching '{question}'. Please try a different search or use the filters above."

    # Format college information
    colleges = format_college_info(retrieved_chunks)
    
    if not colleges:
        return "No college information found. Please try a different search."

    # Build a clean prompt
    college_list = []
    for i, college in enumerate(colleges[:5], 1):
        college_list.append(f"{i}. **{college['name']}**")
        college_list.append(f"   📍 Location: {college['location']}")
        college_list.append(f"   📚 Course: {college['course']}")
        college_list.append(f"   💰 Fee: {college['fee']}")
        college_list.append("")
    
    context = "\n".join(college_list)
    
    # Simple, clean prompt
    prompt = f"""Based on this college information, answer the question.

COLLEGES:
{context}

QUESTION: {question}

Give a helpful, concise answer recommending specific colleges from the list above. If asking for best college, recommend 2-3 options with brief reasons."""

    response = generate_ai_response(prompt)
    
    # If response is empty or too short, provide fallback
    if len(response) < 50:
        response = f"Here are some colleges for your search:\n\n{context}"
    
    return response