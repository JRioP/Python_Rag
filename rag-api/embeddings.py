import os
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings


def get_embeddings():
    """Same all-MiniLM-L6-v2 model as before, via ONNX (no PyTorch)."""
    return FastEmbedEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        cache_dir=os.getenv("FASTEMBED_CACHE", "./models"),
    )
