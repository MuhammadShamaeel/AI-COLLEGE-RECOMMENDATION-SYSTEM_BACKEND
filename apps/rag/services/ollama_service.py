import ollama


# Model name — change to whichever model you have pulled locally,
# e.g. "mistral", "phi3", "gemma2", etc.
OLLAMA_MODEL = "mistral"


def generate_ai_response(prompt: str) -> str:
    """
    Send a prompt to the local Ollama instance and return the text reply.

    FIX: wrapped in try/except so a missing or crashed Ollama process
    returns a clear error message instead of an unhandled 500 exception
    reaching the frontend.
    """

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CampusIQ, a helpful college recommendation assistant. "
                        "Answer only from the provided context. "
                        "Be factual, clear, and concise."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response["message"]["content"]

    except ollama.ResponseError as exc:
        print(f"[ollama_service] Ollama ResponseError: {exc}")
        return (
            f"The AI model returned an error: {exc}. "
            "Please ensure the model is pulled (`ollama pull llama3`)."
        )

    except Exception as exc:
        print(f"[ollama_service] Unexpected error: {exc}")
        return (
            "The AI service is currently unavailable. "
            "Please make sure Ollama is running (`ollama serve`) and try again."
        )