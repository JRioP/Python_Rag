import os
import pandas as pd
from langchain_community.document_loaders import (
    PyPDFLoader, Docx2txtLoader, TextLoader, DataFrameLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from embeddings import get_embeddings

DOCS_FOLDER = "./docs"
DB_FOLDER = "./chroma_db"


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
            docs.extend(DataFrameLoader(df, page_content_column="text").load())
    print(f"Loaded {len(docs)} document pages.")
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
    return chunks


def build_db():
    chunks = split_documents(load_documents(DOCS_FOLDER))
    Chroma.from_documents(chunks, get_embeddings(), persist_directory=DB_FOLDER)
    print("chroma_db built.")


if __name__ == "__main__":
    build_db()
