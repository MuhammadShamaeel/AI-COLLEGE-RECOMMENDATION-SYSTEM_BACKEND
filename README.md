# CampusIQ — AI College Recommendation System (Backend)

An AI-powered college discovery and course assistance platform built with Django REST Framework, Retrieval-Augmented Generation (RAG), FAISS vector search, and Ollama LLM.

Students can search colleges by course and location, view fee structures, and get intelligent answers to their queries through an AI chatbot powered by real college data.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Database | PostgreSQL |
| Authentication | JWT (SimpleJWT) |
| AI / NLP | LangChain, Sentence Transformers |
| Vector Database | FAISS |
| LLM | Ollama (mistral) |
| Embeddings | all-MiniLM-L6-v2 (HuggingFace) |

---

## Project Structure

```
backend/
│
├── apps/
│   ├── users/               # Auth — register, login, profile
│   ├── colleges/            # College & course listing, search, filtering
│   ├── chatbot/             # Chat sessions, message history, AI replies
│   └── rag/
│       ├── services/
│       │   ├── csv_loader.py        # Load and parse college CSV data
│       │   ├── text_splitter.py     # Chunk documents for embedding
│       │   ├── embedding_service.py # Generate sentence embeddings
│       │   ├── vector_store.py      # Save/load FAISS index
│       │   ├── retrieval_service.py # Semantic similarity search
│       │   ├── rag_pipeline.py      # Full RAG orchestration
│       │   ├── ollama_service.py    # Ollama LLM integration
│       │   └── text_cleaner.py      # Text preprocessing
│       └── management/
│           └── commands/
│               ├── process_csv.py   # Build vector DB from CSV
│               ├── test_chatbot.py  # CLI chatbot test
│               └── test_retrieval.py # CLI retrieval test
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── data/
│   └── College_Fees_Master_2026-27.csv
│
├── vector_db/               # Auto-generated — not committed to git
│   ├── college_index.faiss
│   └── chunks.pkl
│
├── media/                   # User uploads — not committed to git
├── manage.py
├── requirements.txt
└── .env                     # Not committed to git
```

---

## API Endpoints

### Users
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/users/register/` | No | Register new user |
| POST | `/api/users/login/` | No | Login, returns JWT tokens |
| POST | `/api/users/token/refresh/` | No | Refresh access token |
| GET / PUT | `/api/users/profile/` | Yes | View or update profile |

### Colleges
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/colleges/` | No | List all colleges |
| GET | `/api/colleges/?course=CSE&location=Kerala&state=Kerala` | No | Search/filter colleges |
| GET | `/api/colleges/<id>/` | No | College detail |
| GET | `/api/colleges/<id>/courses/` | No | All courses of a college |

### Chatbot
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/chatbot/chat/` | Yes | Send message, get AI reply |
| GET | `/api/chatbot/sessions/` | Yes | List all chat sessions |
| GET | `/api/chatbot/sessions/<id>/` | Yes | Full message history of a session |
| DELETE | `/api/chatbot/sessions/<id>/` | Yes | Delete a session |

---

## RAG Pipeline Flow

```
CSV Data
    ↓
Text Extraction & Cleaning
    ↓
Document Chunking (chunk_size=800, overlap=150)
    ↓
Sentence Embedding (all-MiniLM-L6-v2)
    ↓
FAISS Vector Index Storage
    ↓
          ← User Query
          ← Query Embedding
          ← Similarity Search (L2 distance threshold)
          ← Optional Location Filter
          ← Relevant Chunks Retrieved
          ↓
Ollama LLM (mistral) Prompt Generation
    ↓
AI Response → User
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd backend
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull the LLM model
ollama pull mistral

# Start Ollama server
ollama serve
```

### 5. Configure environment variables

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=college_ai_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser (for Django admin)

```bash
python manage.py createsuperuser
```

### 8. Build the vector database

```bash
python manage.py process_csv
```

This reads `data/College_Fees_Master_2026-27.csv`, generates embeddings, and saves the FAISS index to `vector_db/`. Run this again any time the CSV data changes.

### 9. Start the development server

```bash
python manage.py runserver
```

Server runs at `http://localhost:8000`

---

## Testing

### Test the chatbot from the terminal

```bash
python manage.py test_chatbot
```

### Test semantic retrieval

```bash
python manage.py test_retrieval
```

### Test via Django shell

```bash
python manage.py shell
```

```python
from apps.rag.services.rag_pipeline import ask_college_assistant

response = ask_college_assistant("B.Tech CSE colleges in Kerala with fees")
print(response)
```

---

## Django Admin

Access the admin panel at `http://localhost:8000/admin/` after creating a superuser.

From admin you can view and manage:
- Users and profiles
- Colleges and courses
- Chat sessions and messages

---

## Future Enhancements

- PDF brochure upload and processing
- Personalized college recommendations
- Advanced AI ranking system
- Multi-language chatbot support
- Docker deployment setup
- Cloud deployment (AWS / GCP)

---

## Contributors

- Archana K
- Muhammed Shamaeel K M

---

## License

This project is developed for educational and internship purposes.