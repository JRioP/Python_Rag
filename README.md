# 🧠 Python RAG — FastAPI Microservice on Render

A lightweight Retrieval-Augmented Generation (RAG) backend service that lets you chat with your documents. Built with LangChain and FastAPI, optimized for Render's free web service using ONNX embeddings via **FastEmbed** and a pre-indexed **ChromaDB** vector store built at image build time. Inference is powered by Groq.

---

## ✨ Features

- 🌐 **FastAPI Backend**: Exposes `/chat` (with optional API key header protection) and `/health` endpoints.
- 🚀 **Free Cloud Hosting**: Deployed on Render's free tier ($0/month, no credit card required).
- ⚡ **FastEmbed ONNX Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` via ONNX Runtime without PyTorch bloat, fitting comfortably within Render's 512 MB memory limit.
- 🏗️ **Build-Time Vector Indexing**: ChromaDB is built during Docker build (`python ingest.py`), eliminating database indexing latency during server startup.
- 📄 **Multi-Format Ingestion**: Supports PDF, DOCX, TXT, and XLSX files.
- 🔒 **Shared-Secret Security**: Optional `X-Api-Key` header authentication to protect `/chat` from unauthorized quota usage.

---

## 🗂️ Project Structure

```
Python_Rag/
├── .gitignore            # UTF-8 clean ignore rules
├── README.md             # Project documentation
└── rag-api/
    ├── Dockerfile        # Render container definition with build-time ingestion
    ├── .dockerignore     # Excludes .env, local caches, and private documents
    ├── main.py           # FastAPI app with health check & authenticated /chat
    ├── rag.py            # LangChain retrieval & Groq chat pipeline (with build-if-missing fallback)
    ├── ingest.py         # Standalone build-time document ingestion into ChromaDB
    ├── embeddings.py     # FastEmbed ONNX embedding generator
    ├── requirements.txt  # Slim dependencies (no PyTorch)
    ├── docs/             # Knowledge base documents
    ├── docs_private/     # Gitignored & dockerignored folder for private documents
    └── .env              # Local environment variables (never committed)
```

---

## 🚀 Local Development

### 1. Prerequisites

- Python 3.10+ (tested on Python 3.11–3.14)
- A free API key from [Groq Console](https://console.groq.com/)

### 2. Install Dependencies

Navigate into `rag-api/` and install dependencies:

```bash
cd rag-api
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file inside `rag-api/`:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
# Optional overrides:
MODEL=openai/gpt-oss-20b
# API_KEY=your_optional_secret_here
```

### 4. Build the Vector Store

Before running the server locally, index the documents in `docs/`:

```bash
python ingest.py
```

*(Note: If `chroma_db` is missing when starting the server, `rag.py` includes a fallback that automatically builds it on first run).*

### 5. Start the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

---

## 💬 API Endpoints

### `GET /health`
Uptime health check (unauthenticated). Returns:
```json
{ "status": "healthy", "service": "rag-api" }
```

### `POST /chat`
Accepts a JSON payload with a question. If `API_KEY` is configured in environment, requires the `X-Api-Key` header.
```bash
curl -X POST "http://localhost:8080/chat" \
     -H "Content-Type: application/json" \
     -H "X-Api-Key: your_secret_key" \
     -d '{"question": "What is RoadRescue?"}'
```

Response:
```json
{
  "answer": "RoadRescue is a native Android roadside assistance app..."
}
```

---

## ☁️ Deployment on Render

1. Create a new **Web Service** on [dashboard.render.com](https://dashboard.render.com).
2. Connect your repository (`JRioP/Python_Rag`).
3. Set the following options:
   - **Name**: `python-rag`
   - **Region**: `Ohio (US East)` or `Virginia (US East)`
   - **Branch**: `render-migration`
   - **Root Directory**: `rag-api`
   - **Runtime**: `Docker`
   - **Instance Type**: `Free`
4. Add environment variables:
   - `GROQ_API_KEY`: *(paste your Groq API key)*
   - `API_KEY`: *(optional shared secret for proxy authorization)*
5. Set **Health Check Path** to `/health`.
6. Click **Create Web Service**.

---

## 📝 License

MIT License — free to use and modify.