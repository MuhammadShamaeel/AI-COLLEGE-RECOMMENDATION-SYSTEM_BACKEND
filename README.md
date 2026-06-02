# EduNova — AI College Recommendation System (Backend)

An AI-powered college discovery and course assistance platform built with Django REST Framework, Retrieval-Augmented Generation (RAG), FAISS vector search, and Ollama LLM.

Students can search colleges by course, state, and location, view fee structures, and get intelligent answers through an AI chatbot powered by real college data.

---

## Tech Stack

| Layer | Technology |
|---------|------------|
| Backend | Python 3.13+, Django 6.0, Django REST Framework |
| Database | SQLite (Default) / PostgreSQL (Production) |
| Authentication | JWT (SimpleJWT) |
| AI / NLP | Sentence Transformers |
| Vector Database | FAISS |
| LLM | Ollama (TinyLlama / Llama 3.2 / Mistral) |
| Embeddings | all-MiniLM-L6-v2 |

---

## Project Structure

```text
backend/
│
├── apps/
│   ├── users/
│   ├── colleges/
│   ├── chatbot/
│   └── rag/
│       ├── services/
│       │   ├── csv_loader.py
│       │   ├── text_splitter.py
│       │   ├── embedding_service.py
│       │   ├── vector_store.py
│       │   ├── retrieval_service.py
│       │   ├── rag_pipeline.py
│       │   ├── ollama_service.py
│       │   └── text_cleaner.py
│       │
│       └── management/
│           └── commands/
│               ├── process_csv.py
│               ├── test_chatbot.py
│               └── test_retrieval.py
│
├── config/
├── data/
│   └── College_Fees_Master_2026-27.csv
│
├── vector_db/
├── media/
├── manage.py
├── requirements.txt
└── .env
```

---

## API Endpoints

### Users

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/api/users/register/` | Register user |
| POST | `/api/users/login/` | Login and receive JWT |
| POST | `/api/users/token/refresh/` | Refresh JWT token |
| GET / PUT | `/api/users/profile/` | View or update profile |

### Colleges

| Method | Endpoint | Description |
|----------|-----------|-------------|
| GET | `/api/colleges/` | List colleges |
| GET | `/api/colleges/filters/` | Available filters |
| GET | `/api/colleges/<id>/` | College details |
| GET | `/api/colleges/<id>/courses/` | College courses |

Example:

```http
GET /api/colleges/?course=BCA&state=Kerala
```

### Chatbot

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/api/chatbot/chat/` | Send query to AI |
| GET | `/api/chatbot/sessions/` | List sessions |
| GET | `/api/chatbot/sessions/<id>/` | Session history |
| DELETE | `/api/chatbot/sessions/<id>/` | Delete session |

---

## RAG Pipeline Flow

```text
College CSV Data
        │
        ▼
Text Cleaning
        │
        ▼
Document Chunking
        │
        ▼
Sentence Embeddings
        │
        ▼
FAISS Vector Storage
        │
        ▼
Similarity Search
        │
        ▼
Relevant Context Retrieval
        │
        ▼
Ollama LLM
        │
        ▼
AI Response
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/MuhammadShamaeel/AI-COLLEGE-RECOMMENDATION-SYSTEM_BACKEND.git

cd AI-COLLEGE-RECOMMENDATION-SYSTEM_BACKEND
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download from:

https://ollama.com

Pull a model:

```bash
ollama pull tinyllama
```

or

```bash
ollama pull llama3.2:3b
```

or

```bash
ollama pull mistral
```

Start Ollama:

```bash
ollama serve
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Build Vector Database

```bash
python manage.py process_csv
```

### 9. Run Development Server

```bash
python manage.py runserver
```

Backend URL:

```text
http://localhost:8000
```

---

## Testing

### Chatbot Test

```bash
python manage.py test_chatbot
```

### Retrieval Test

```bash
python manage.py test_retrieval
```

### Django Shell Test

```bash
python manage.py shell
```

```python
from apps.rag.services.rag_pipeline import ask_college_assistant

response = ask_college_assistant(
    "BCA colleges in Kerala with fees"
)

print(response)
```

---

## API Testing

### Search Colleges

```bash
curl "http://localhost:8000/api/colleges/?course=BCA&state=Kerala"
```

### Get Filters

```bash
curl "http://localhost:8000/api/colleges/filters/"
```

### Chat with AI

```bash
curl -X POST http://localhost:8000/api/chatbot/chat/ \
-H "Content-Type: application/json" \
-d '{"message":"Tell me about BCA colleges in Kerala"}'
```

---

## Django Admin

```text
http://localhost:8000/admin/
```

Manage:

- Users
- Profiles
- Colleges
- Courses
- Chat Sessions
- Messages

---

## Environment Variables

| Variable | Description |
|------------|-------------|
| SECRET_KEY | Django secret key |
| DEBUG | Debug mode |
| ALLOWED_HOSTS | Allowed hosts |
| DB_NAME | Database name |
| DB_USER | Database username |
| DB_PASSWORD | Database password |
| DB_HOST | Database host |
| DB_PORT | Database port |

---

## Troubleshooting

### Ollama Not Running

```bash
curl http://localhost:11434
```

Restart:

```bash
ollama serve
```

### Missing Vector Database

```bash
python manage.py process_csv
```

### Module Errors

```bash
pip install -r requirements.txt
```

---

## Future Enhancements

- Personalized recommendations
- College ranking system
- PDF processing
- Multi-language chatbot
- Docker support
- Cloud deployment

---

## Contributors

**Muhammed Shamaeel K M**
- Frontend Development
- UI/UX Design

**Archana K**
- Backend Development
- RAG Pipeline

---

## License

Educational Project.

---

## Repository Links

Frontend Repository:
https://github.com/MuhammadShamaeel/AI-COLLEGE-RECOMMENDATION-SYSTEM_FRONTEND

Backend Repository:
https://github.com/MuhammadShamaeel/AI-COLLEGE-RECOMMENDATION-SYSTEM_BACKEND