# services/chroma_db_client.py
import uuid
import os
from chromadb import PersistentClient

# ------------------------------
# Setup persistence directory
# ------------------------------
CHROMA_PERSIST_DIR = "./chroma_db"
os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)

# ------------------------------
# Initialize ChromaDB client
# ------------------------------
chroma_client = PersistentClient(path=CHROMA_PERSIST_DIR)

# ------------------------------
# Create or get collection
# ------------------------------
def get_collection(name: str = "file_texts"):
    """
    Return a Chroma collection by name, creating it if it doesn't exist.
    Now generalized for any text file (PDF, Word, Image text, etc.)
    """
    try:
        existing_collections = [c.name for c in chroma_client.list_collections()]
        if name in existing_collections:
            return chroma_client.get_collection(name)
        else:
            return chroma_client.create_collection(
                name=name,
                metadata={"description": "Text extracted from uploaded files"}
            )
    except Exception as e:
        print(f"Error getting or creating collection '{name}': {e}")
        return None

collection = get_collection()
if collection is None:
    raise RuntimeError("Could not retrieve or create the ChromaDB collection.")

# ------------------------------
# Add text to ChromaDB
# ------------------------------
def add_to_chromadb(file_id: str, text: str, vector: list):
    """
    Add extracted text with its embedding vector to ChromaDB.
    Generates a unique ID per chunk to handle multiple chunks per file.
    """
    try:
        unique_id = f"{file_id}_{uuid.uuid4()}"
        collection.add(
            documents=[text],
            metadatas=[{"file_id": file_id}],
            ids=[unique_id],
            embeddings=[vector]
        )
        return True
    except Exception as e:
        print(f"[ERROR] ChromaDB add error: {e}")
        return False

# ------------------------------
# Query ChromaDB for relevant text
# ------------------------------
def query_chromadb(file_id: str, query: str, top_k: int = 3, embedding_model=None):
    """
    Retrieve top-k relevant text chunks for a query.
    embedding_model: instance of EmbeddingModel
    """
    try:
        if embedding_model is None:
            raise ValueError("embedding_model must be provided for vector search")

        query_vector = embedding_model.get_embedding(query)
        if query_vector is None:
            return []

        results = collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where={"file_id": file_id}
        )

        hits = []
        for doc_id, doc_text, meta in zip(
            results["ids"][0], results["documents"][0], results["metadatas"][0]
        ):
            hits.append({"id": doc_id, "text": doc_text, "metadata": meta})

        return hits

    except Exception as e:
        print(f"[ERROR] ChromaDB query error: {e}")
        return []
