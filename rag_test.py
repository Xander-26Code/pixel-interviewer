from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi import APIRouter


router = APIRouter()

class RagRequest(BaseModel):
    question: str
    markdowns: list[str]
    top_k: int = 3

def split_text(text: str, chunk_size: int = 250, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

def embedding_text(text: list[str], question: str, top_k: int = 3) -> list[dict]:
    chunk_vectors = model.encode(
        text,
        normalize_embeddings=True,
    )

    scores = chunk_vectors @ model.encode(question, normalize_embeddings=True)
    ranked_indexes = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indexes:
        results.append(
            {
                "score": float(scores[index]),
                "chunk": text[index],
            }
        )

    return results

def build_chunk(markdowns: list[str]) -> list[str]:
    records = []
    for markdown in markdowns:
        chunks = split_text(markdown)
        records.extend(chunks)
    return records

@router.post("/rag")
def retrieve(request: RagRequest):
    chunks = build_chunk(request.markdowns)
    results = embedding_text(chunks, request.question, request.top_k)
    return results
