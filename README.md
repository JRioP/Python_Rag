# 🧠 Python RAG — FastAPI Microservice

A Retrieval-Augmented Generation (RAG) backend service that lets you chat with your own documents. This project wraps a LangChain pipeline in a FastAPI server, utilizing a local ChromaDB vector store and lightning-fast cloud inference via the Groq API.

---

## ✨ Features

- 🌐 **RESTful API**: Exposes `/chat` and `/health` endpoints using FastAPI.
- 🚀 **Cloud Inference**: Powered by **Groq** (`llama-3.1-8b-instant`) for extremely fast, production-ready responses.
- 📄 **Multi-Format Support**: Reads PDF, DOCX, TXT, and XLSX files.
- 🔍 **Semantic Search**: Uses HuggingFace Embeddings (`all-MiniLM-L6-v2`).
- 🗄️ **Persistent Vector Store**: Auto-loads existing ChromaDB on startup (no re-embedding needed).
- ☁️ **Deployment Ready**: Includes a `Procfile` and structured for seamless cloud hosting (e.g., Railway).

---

## 🗂️ Project Structure

My_RAG/
└── rag-api/
    ├── docs/              # 📁 Put your documents here
    ├── chroma_db/         # 🗄️ Auto-generated vector store
    ├── main.py            # 🌐 FastAPI server & endpoints
    ├── rag.py             # 🤖 LangChain & ChromaDB logic
    ├── requirements.txt   # 📦 Dependencies for deployment
    ├── Procfile           # ☁️ Cloud deployment config
    └── .env               # 🔑 Your Groq API key (not tracked in Git)

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- A free API key from [Groq Console](https://console.groq.com/)

### 2. Set Up the Environment

Navigate to the API folder and install the required dependencies:

cd rag-api
pip install -r requirements.txt

*(If you are setting this up manually without the requirements file, run: `pip install fastapi uvicorn pydantic langchain langchain-groq langchain-chroma pandas openpyxl langchain-community pypdf docx2txt langchain-huggingface sentence-transformers python-dotenv`)*

### 3. Configure API Keys

Create a `.env` file inside the `rag-api/` directory and add your Groq API key:

GROQ_API_KEY=gsk_your_actual_key_here

### 4. Add Your Documents

Drop your files into the `rag-api/docs/` folder:

docs/
├── appraisal.pdf
├── training_plan.xlsx
└── weekly_journal.pdf

### 5. Start the Server

Run the FastAPI server using Uvicorn:

uvicorn main:app --reload

On the first run, the server will embed your documents and save them to `chroma_db/`. On subsequent runs, it loads instantly into memory.

---

## 💬 Usage & Testing

Because this is an API, there is no terminal chat loop. You interact with it via HTTP requests.

### Test via Swagger UI (Browser)
FastAPI automatically generates an interactive testing dashboard.
1. Open your browser to `http://127.0.0.1:8000/docs`
2. Expand the **POST `/chat`** endpoint.
3. Click **Try it out**, enter your question in the JSON body, and click **Execute**.

### Test via cURL (Terminal)

curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d "{\"question\": \"What is the summary of the report?\"}"


**Example Response:**

{
  "answer": "Based on the provided context, the report discusses..."
}


---

## ⚙️ Configuration

You can adjust these settings at the top of `rag-api/rag.py`:

| Variable | Default | Description |
|---|---|---|
| `DOCS_FOLDER` | `./docs` | Folder containing your documents |
| `DB_FOLDER` | `./chroma_db` | Where the vector store is saved |
| `MODEL` | `llama-3.1-8b-instant` | Groq model used for inference |

---

## 🛠️ Built With

| Tool | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework for the API |
| [LangChain](https://www.langchain.com/) | RAG pipeline & document loading |
| [Groq](https://groq.com/) | High-speed LLM inference |
| [ChromaDB](https://www.trychroma.com/) | Local vector database |
| [HuggingFace](https://huggingface.co/) | Text embeddings (`all-MiniLM-L6-v2`) |

---

## 📝 License

MIT License — free to use and modify.