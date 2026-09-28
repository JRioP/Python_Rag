import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from embeddings import get_embeddings

DB_FOLDER = "./chroma_db"
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

if not os.path.isdir(DB_FOLDER):
    print("chroma_db not found; building it now (slow). In Docker this happens at build time.")
    from ingest import build_db
    build_db()

db = Chroma(persist_directory=DB_FOLDER, embedding_function=get_embeddings())
llm = ChatGroq(model=MODEL, temperature=0)
retriever = db.as_retriever(search_kwargs={"k": 25})

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


def ask_rag(question: str) -> str:
    return chain.invoke(question)