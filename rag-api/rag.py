import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

DOCS_FOLDER = "./docs"
DB_FOLDER = "./chroma_db"
MODEL = "llama-3.1-8b-instant"

# Load all documents
def load_documents(folder):
    docs = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if filename.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
        elif filename.endswith(".docx"):
            docs.extend(Docx2txtLoader(path).load())
        elif filename.endswith(".txt"):
            docs.extend(TextLoader(path, encoding="utf-8").load())
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(path, dtype=str).fillna("")
            df["text"] = df.apply(lambda row: " | ".join(row.values), axis=1)
            loader = DataFrameLoader(df, page_content_column="text")
            docs.extend(loader.load())
            
    print(f"Loaded {len(docs)} document pages.")
    return docs

# Split into chunks
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

# Embed and store
def create_vectorstore(chunks):
    print("Embedding documents... (this may take a minute)")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(chunks, embeddings, persist_directory=DB_FOLDER)
    print("Vector store created!")
    return db

# Load existing store
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_FOLDER, embedding_function=embeddings)
    return db


# --- FastAPI Integration ---
# This block runs once when the FastAPI server starts up.

if os.path.exists(DB_FOLDER):
    print("Loading existing vector store...")
    db = load_vectorstore()
else:
    docs = load_documents(DOCS_FOLDER)
    chunks = split_documents(docs)
    db = create_vectorstore(chunks)

# Initialize Groq LLM instead of Ollama
llm = ChatGroq(model=MODEL, temperature=0)

# Set up the retriever and prompt
retriever = db.as_retriever(search_kwargs={"k": 25})

prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context:
{context}

Question: {question}
""")

# Build the LCEL chain globally
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def ask_rag(question: str) -> str:
    """
    Takes a string question from the FastAPI endpoint, runs it through 
    the RAG pipeline, and returns the string answer.
    """
    # The chain.invoke handles the whole pipeline and returns the string output
    return chain.invoke(question)