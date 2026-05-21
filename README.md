# AI College Recommendation System - Backend

An AI-powered college discovery and recommendation platform backend built using Django, Django REST Framework, Retrieval-Augmented Generation (RAG), FAISS, and Ollama.

The system helps students discover colleges based on courses and locations while providing intelligent AI-generated answers from college brochure PDFs using semantic search and conversational AI.

---

# Features

- AI-powered college recommendation system
- Retrieval-Augmented Generation (RAG) pipeline
- College brochure PDF processing
- Semantic search using FAISS vector database
- AI chatbot for student queries
- Course and location-based college search
- JWT Authentication system
- REST API architecture
- PDF text extraction and chunking
- Embedding generation using Sentence Transformers
- Ollama LLM integration
- Metadata-based filtering
- Scalable backend architecture

---

# Tech Stack

## Backend
- Python
- Django
- Django REST Framework

## Database
- PostgreSQL

## AI / NLP
- LangChain
- Sentence Transformers
- SpaCy
- NLTK

## RAG Components
- FAISS Vector Database
- Recursive Text Splitter
- Embedding Models

## LLM
- Ollama

## Authentication
- JWT Authentication

---

# Project Architecture

```text
User Query
    ↓
Django REST API
    ↓
RAG Pipeline
    ↓
Semantic Retrieval (FAISS)
    ↓
Relevant PDF Chunks
    ↓
Ollama LLM
    ↓
AI Generated Response
```

---

# Folder Structure

```text
backend/
│
├── apps/
│   ├── users/
│   ├── colleges/
│   ├── chatbot/
│   └── rag/
│       ├── services/
│       ├── management/
│       └── utils/
│
├── config/
├── media/
├── vector_store/
├── requirements.txt
└── manage.py
```

---

# RAG Pipeline Workflow

## PDF Processing
- Load college brochure PDFs
- Extract text from PDFs
- Clean and preprocess text
- Split text into chunks
- Generate embeddings
- Store embeddings in FAISS vector database

## AI Retrieval Flow
- User submits query
- Query converted into embedding
- FAISS performs similarity search
- Relevant chunks retrieved
- Context sent to Ollama
- AI generates final response

---

# Authentication Features

- User Registration
- User Login
- JWT Access Tokens
- JWT Refresh Tokens
- User Profile APIs

---

# API Modules

## Authentication APIs
- Register API
- Login API
- Refresh Token API
- User Profile API

## College APIs
- College Listing
- College Details
- Course Search
- Location Filtering

## AI Chatbot APIs
- RAG-based Query Answering
- Semantic Search
- Conversational AI Responses

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
cd backend
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / Mac
```bash
source venv/bin/activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=college_ai_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

# Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Run Server

```bash
python manage.py runserver
```

---

# RAG Commands

## Process PDFs

```bash
python manage.py process_pdfs
```

## Test Semantic Retrieval

```bash
python manage.py test_retrieval
```

---

# Future Enhancements

- Personalized college recommendations
- Advanced AI ranking system
- Multi-language chatbot
- Chat history storage
- Recommendation scoring system
- Admin dashboard
- Deployment with Docker
- Cloud deployment support

---

# Contributors

- Archana K
- Muhammed Shamaeel K M

---

# License

This project is developed for educational and internship purposes.