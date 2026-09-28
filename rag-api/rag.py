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

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are Josh's portfolio AI assistant — friendly, articulate, and concise.
Your job is to answer questions about Josh's projects, technical skills, background, and experience based ONLY on the context provided below.

Formatting guidelines:
- Start with a direct 1–2 sentence overview answering the question.
- Follow up with 2–4 short, clear bullet points highlighting key details, technologies, or achievements.
- DO NOT use markdown tables (they look cramped in small chat popups). Always use bullet points instead.
- Keep the total response concise (under 120 words) and easy to scan on mobile.
- If the question cannot be answered from the context, politely say: "I don't have that specific detail in Josh's project documents, but feel free to reach out to him directly through the contact page!"

Context:
{context}""",
    ),
    ("human", "{question}"),
])

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


def ask_rag(question: str) -> str:
    return chain.invoke(question)