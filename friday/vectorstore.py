"""
Thin wrapper around ChromaDB. Each course (e.g. "JEE Physics - Mechanics",
"MBOSE Class 12 Chemistry") gets its own Chroma collection so retrieval
stays scoped to the right subject instead of mixing everything together.
"""

import uuid
import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DIR, EMBEDDING_MODEL

_client = chromadb.PersistentClient(path=CHROMA_DIR)
_embedder = SentenceTransformer(EMBEDDING_MODEL)


def _collection_name(course_id: str) -> str:
    return f"course_{course_id}"


def add_chunks(course_id: str, chunks: list[str], source_name: str) -> int:
    collection = _client.get_or_create_collection(_collection_name(course_id))
    embeddings = _embedder.encode(chunks).tolist()
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": source_name} for _ in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)


def query(course_id: str, question: str, n_results: int = 5) -> list[dict]:
    collection = _client.get_or_create_collection(_collection_name(course_id))
    q_embedding = _embedder.encode([question]).tolist()

    results = collection.query(
        query_embeddings=q_embedding,
        n_results=min(n_results, max(collection.count(), 1)),
    )

    hits = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    for doc, meta in zip(docs, metas):
        hits.append({"text": doc, "source": meta.get("source", "unknown")})
    return hits


def list_courses() -> list[str]:
    return [c.name.replace("course_", "", 1) for c in _client.list_collections()]


def delete_course(course_id: str) -> None:
    _client.delete_collection(_collection_name(course_id))
