import ollama
import logging
import re

logger = logging.getLogger(__name__)

# Use a better model - pull it first: ollama pull llama3.2:3b
OLLAMA_MODEL = "llama3.2:3b"


def clean_response(response: str) -> str:
    """Clean up the response by removing any prompt instructions."""
    # Remove common prompt patterns
    patterns = [
        r'You are EduNova AI.*?(?=\n\n|\Z)',
        r'Guidelines:.*?(?=\n\n|\Z)',
        r'CONTEXT.*?(?=\n\n|\Z)',
        r'QUESTION:.*?(?=\n\n|\Z)',
        r'Answer the student\'s question.*?(?=\n\n|\Z)',
    ]
    
    for pattern in patterns:
        response = re.sub(pattern, '', response, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove any remaining "---" separators
    response = re.sub(r'=+\n', '', response)
    
    return response.strip()


def generate_ai_response(prompt: str) -> str:
    """
    Generate a response using Ollama.
    """
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are EduNova AI, a college admissions advisor. Give short, helpful answers based ONLY on the information provided. Be direct and concise. Never repeat the instructions or context back to the user."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.3,
                "num_predict": 300,
                "top_p": 0.9,
            }
        )
        
        result = response["message"]["content"]
        return clean_response(result)

    except Exception as exc:
        logger.error(f"Ollama error: {exc}")
        return "I'm having trouble connecting right now. Please try again in a moment."