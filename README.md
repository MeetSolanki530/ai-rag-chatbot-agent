# AI RAG Chatbot – Bhagavata Knowledge Assistant

## Project Overview

This project is a **Retrieval-Augmented Generation (RAG) based AI chatbot** designed to answer questions from **Bhagavata Purana texts**.

The system uses **Large Language Models (LLMs)** combined with **vector similarity search** to retrieve relevant passages from stored documents and generate accurate answers.

Unlike traditional chatbots, the model **does not rely solely on pretrained knowledge**. Instead, it dynamically retrieves information from a **document knowledge base stored as embeddings**.

Although this implementation focuses on **Bhagavata Purana**, the system is designed as a **reusable RAG framework**. Any user can replace the document folder with different PDFs or text documents to build a chatbot for another domain.

The application provides a **ChatGPT-style web interface with streaming responses**, allowing users to interact with the knowledge base in real time while also viewing the **retrieved context used to generate the answer**.

---

# Key Features

### Domain Knowledge via Documents

The chatbot retrieves answers directly from uploaded **document sources such as PDFs** stored in a data folder.

The system can easily be adapted to other domains by replacing the document dataset.

---

### Reusable RAG Framework

The architecture is designed to work with **any document collection**, not just Bhagavata Purana texts.

Users can simply add new files to the **documents folder**, re-run indexing, and deploy a new domain-specific chatbot.

---

### Retrieval Augmented Generation (RAG)

User queries are converted into embeddings and matched against stored document vectors to retrieve the most relevant passages.

These passages are used as context for generating the final answer.

---

### Streaming Responses

Responses are streamed from the backend using **FastAPI asynchronous streaming**.

This enables:

* Faster perceived response time
* Smooth token-by-token response generation
* Improved user experience

---

### Async Backend Architecture

The system uses **FastAPI async endpoints** to efficiently handle:

* User queries
* Retrieval operations
* LLM response streaming

This ensures the application remains **responsive even during long LLM responses**.

---

### Context Transparency

The frontend displays:

* The generated answer
* The retrieved document context

This allows users to **verify the source of the response** and improves trust in the system.

---

### ChatGPT-style UI

Frontend interface built using:

* HTML
* CSS
* JavaScript

Features include:

* Interactive chat interface
* Streaming AI responses
* Scrollable conversation history
* Context display panel

---

### Future Enhancements

Planned improvements include:

* MongoDB chat history persistence
* User authentication
* Multi-user sessions
* Hybrid search (keyword + vector retrieval)

---

# Tech Stack

| Component       | Technology                           |
| --------------- | ------------------------------------ |
| Backend         | FastAPI                              |
| LLM Framework   | LangChain                            |
| Vector Database | Pinecone                             |
| Embeddings      | OpenAI / HuggingFace                 |
| Frontend        | HTML, CSS, JavaScript                |
| Deployment      | Vercel / Cloud                       |
| Future Database | MongoDB                              |
| Architecture    | Retrieval-Augmented Generation (RAG) |

---

# System Architecture

```
User
  ↓
Frontend (Chat Interface)
  ↓
FastAPI Backend
  ↓
Async Query Handler
  ↓
RAG Retrieval Pipeline
  ↓
Vector Database (Pinecone)
  ↓
Relevant Document Context
  ↓
LLM Response Generation
  ↓
Streaming Response
  ↓
Frontend Display (Answer + Context)
```

---

# Project Workflow

## 1. Document Ingestion

The system reads documents from a **local data folder**.

Example supported formats:

* PDF
* TXT
* Markdown
* HTML (optional)

Example directory:

```
data/documents/
```

Users can add new documents to this folder to expand the knowledge base.

---

## 2. Document Loading

Documents are loaded using **LangChain document loaders**.

Examples:

* PDF loader
* Text loader
* Directory loader

Each document is converted into structured text.

---

## 3. Text Chunking

Large documents are divided into smaller chunks for efficient retrieval.

Chunking process:

* Split text into segments
* Maintain semantic boundaries
* Attach metadata (source, page number)

Example chunk metadata:

```
{
  "source": "BhagavatPurana_Book1.pdf",
  "page": 12
}
```

Chunking improves retrieval accuracy and reduces token usage.

---

## 4. Embedding Generation

Each text chunk is converted into a **vector embedding**.

Embedding models may include:

* OpenAI embeddings
* HuggingFace sentence-transformers

These embeddings represent **semantic meaning** in vector space.

---

## 5. Vector Index Creation

Generated embeddings are stored inside a **vector database**.

Supported storage options:

* Pinecone (recommended)
* FAISS (local)
* Vercel vector storage

Stored data includes:

```
Embedding vector
Text chunk
Metadata (document name, page, source)
```

---

## 6. Query Processing

When a user submits a question:

1. The query is converted into an embedding.
2. The system searches the vector database.
3. The most relevant document chunks are retrieved.

This ensures the model receives **relevant contextual passages**.

---

## 7. Retrieval-Augmented Generation

Retrieved chunks are inserted into the LLM prompt.

Example prompt structure:

```
Context:
[Retrieved document passages]

Question:
User question

Instruction:
Answer the question using only the provided context.
If the answer is not present, say the information is not available.
```

The LLM then generates the final response.

---

## 8. Streaming Response Generation

FastAPI streams the LLM response using **asynchronous generators**.

Workflow:

1. User sends question
2. FastAPI creates a response job
3. Retrieval pipeline fetches context
4. LLM begins generating tokens
5. Tokens are streamed to frontend

This allows the user to **see the answer being generated live**.

---

## 9. Context Display in Frontend

Along with the answer, the frontend also shows:

* Retrieved text chunks
* Document sources
* Page references

This enables **answer verification and transparency**.

---

## 10. Chat History Handling

Current implementation:

* Chat history stored in **frontend memory**

Future implementation:

* MongoDB storage
* Persistent chat sessions
* Multi-user support

---

# Frontend Design

The frontend provides a **minimal ChatGPT-like interface**.

Core components:

* Chat message container
* User input box
* Send button
* Streaming message display
* Context panel showing retrieved passages

The interface communicates with the backend via **API requests and streaming responses**.

---

# API Endpoints

### Chat Endpoint

```
POST /chat
```

Input:

```
{
  "message": "Who is Prahlada?",
  "history": []
}
```

Response:

Streaming AI response with retrieved context.

---

### Health Check

```
GET /health
```

Used to confirm backend availability.

---

# Project Directory Structure

```
bhagavat-rag-chatbot
│
├── backend
│
│   ├── app
│   │
│   │   ├── main.py
│   │
│   │   ├── api
│   │   │   └── chat.py
│   │
│   │   ├── rag
│   │   │   ├── retriever.py
│   │   │   ├── pipeline.py
│   │   │   └── embeddings.py
│   │
│   │   ├── services
│   │   │   └── llm_service.py
│   │
│   │   ├── utils
│   │   │   └── text_chunker.py
│   │
│   │   └── config
│   │       └── settings.py
│
│   ├── scripts
│   │   └── ingest_documents.py
│
│   └── requirements.txt
│
├── frontend
│
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── data
│   └── documents
│
├── vector_store
│
├── .env
├── .gitignore
└── README.md
```

---

# Environment Variables (.env)

Example configuration:

```
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=us-east-1
PINECONE_INDEX=rag-chatbot
MODEL_NAME=gpt-4
EMBEDDING_MODEL=text-embedding-3-large
```

---

# .gitignore

```
# Python cache
__pycache__/
*.pyc

# Virtual environment
venv/
.env

# Vector store data
vector_store/

# OS files
.DS_Store

# Logs
*.log
```

---

# requirements.txt

Core dependencies:

```
fastapi
uvicorn
langchain
pinecone-client
openai
tiktoken
python-dotenv
pydantic
```

Optional dependencies:

```
faiss-cpu
sentence-transformers
pymongo
pypdf
```
