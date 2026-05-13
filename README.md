# 🧠 Python RAG — Local Document Chatbot

A fully offline Retrieval-Augmented Generation (RAG) chatbot that lets you chat with your own documents. No API keys. No internet. Just your files and a local LLM.

---

## ✨ Features

- 📄 Supports **PDF, DOCX, TXT, and XLSX** files
- 🔍 Semantic search using **HuggingFace Embeddings** (`all-MiniLM-L6-v2`)
- 🗄️ Persistent vector store with **ChromaDB**
- 🤖 Powered by **Ollama** (Llama 3.2) — runs 100% locally
- ⚡ Auto-loads existing vector store on rerun (no re-embedding needed)
- 🌀 Loading spinner for a clean chat experience

---

## 🗂️ Project Structure

```
My_RAG/
├── docs/            # 📁 Put your documents here
├── chroma_db/       # 🗄️ Auto-generated vector store
└── rag.py           # 🤖 Main script
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running
- Llama 3.2 model pulled:

```bash
ollama pull llama3.2
```

### 2. Install Dependencies

```bash
pip install langchain langchain-community langchain-huggingface langchain-ollama chromadb sentence-transformers pandas openpyxl docx2txt pypdf
```

### 3. Add Your Documents

Drop your files into the `docs/` folder:

```
docs/
├── report.pdf
├── notes.docx
├── data.xlsx
└── readme.txt
```

### 4. Run the Chatbot

```bash
python rag.py
```

On first run, it will embed your documents and save them to `chroma_db/`. On subsequent runs, it loads instantly.

---

## 💬 Usage

```
✅ RAG system ready! Type your question (or 'quit' to exit)

You: What is the summary of the report?
🤔 Thinking... ⠋
AI: The report discusses...

You: quit
```

---

## ⚙️ Configuration

You can change these settings at the top of `rag.py`:

| Variable | Default | Description |
|---|---|---|
| `DOCS_FOLDER` | `./docs` | Folder containing your documents |
| `DB_FOLDER` | `./chroma_db` | Where the vector store is saved |
| `MODEL` | `llama3.2:latest` | Ollama model to use |

---

## 🛠️ Built With

| Tool | Purpose |
|---|---|
| [LangChain](https://www.langchain.com/) | RAG pipeline & document loading |
| [ChromaDB](https://www.trychroma.com/) | Local vector store |
| [HuggingFace](https://huggingface.co/) | Text embeddings (`all-MiniLM-L6-v2`) |
| [Ollama](https://ollama.com/) | Local LLM inference |

---

## 📝 License

MIT License — free to use and modify.
