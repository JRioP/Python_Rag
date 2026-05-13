import os
import sys
import threading
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

DOCS_FOLDER = "./docs"
DB_FOLDER = "./chroma_db"
MODEL = "llama3.2:latest"

# --- Step 1: Load all documents ---
def load_documents(folder):
    docs = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if filename.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
        elif filename.endswith(".docx"):
            docs.extend(Docx2txtLoader(path).load())
        elif filename.endswith(".txt"):
            docs.extend(TextLoader(path).load())
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(path, dtype=str).fillna("")
            df["text"] = df.apply(lambda row: " | ".join(row.values), axis=1)
            loader = DataFrameLoader(df, page_content_column="text")
            docs.extend(loader.load())
            
    print(f"Loaded {len(docs)} document pages.")
    return docs

# --- Step 2: Split into chunks ---
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

# --- Step 3: Embed and store ---
def create_vectorstore(chunks):
    print("Embedding documents... (this may take a minute)")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(chunks, embeddings, persist_directory=DB_FOLDER)
    print("Vector store created!")
    return db

# --- Step 4: Load existing store ---
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_FOLDER, embedding_function=embeddings)
    return db

# --- Step 5: Chat loop ---
def chat(db):
    llm = Ollama(model=MODEL)
    retriever = db.as_retriever(search_kwargs={"k": 15})

    prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context:
{context}

Question: {question}
""")

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("\n✅ RAG system ready! Type your question (or 'quit' to exit)\n")
    while True:
        question = input("You: ")
        if question.lower() in ["quit", "exit"]:
            break

        # Loading spinner
        stop_spinner = threading.Event()
        def spinner():
            chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
            i = 0
            while not stop_spinner.is_set():
                print(f"\r🤔 Thinking... {chars[i % len(chars)]}", end="", flush=True)
                i += 1
                threading.Event().wait(0.1)

        t = threading.Thread(target=spinner)
        t.start()

        answer = chain.invoke(question)

        stop_spinner.set()
        t.join()
        print("\r" + " " * 30 + "\r", end="")

        print(f"AI: {answer}\n")

# --- Main ---
if os.path.exists(DB_FOLDER):
    print("Loading existing vector store...")
    db = load_vectorstore()
else:
    docs = load_documents(DOCS_FOLDER)
    chunks = split_documents(docs)
    db = create_vectorstore(chunks)

chat(db)