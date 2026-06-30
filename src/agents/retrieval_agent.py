
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path
 
# ==========================================
# 1. GLOBAL VARIABLES
# ==========================================
 
documents = []
chunked_documents = []
index = None
knowledge_base_name = None
 
# Load the embedding model once, at import time.
# All downstream functions (load_dataset, retrieve) rely on this.
model = SentenceTransformer("all-MiniLM-L6-v2")
 
# ==========================================
# 2. CHUNKING FUNCTION
# ==========================================
 
def chunk_text(text, chunk_size=50):
    words = text.split()
    chunks = []
 
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
 
    return chunks
 
 
# ==========================================
# 3. LOAD DATASET
# ==========================================
 
def load_dataset(dataset):
 
    global documents
    global chunked_documents
    global index
    global knowledge_base_name
 
    documents = dataset
    current_dataset = str(len(dataset))
    if knowledge_base_name == current_dataset and index is not None:
 
        print("Knowledge Base already loaded.")
 
        return
    chunked_documents = []
 
    print(f"\nLoading {len(documents)} historical incidents...")
 
    for doc in documents:
 
        title = (
            doc.get("title")
            or doc.get("event")
            or doc.get("sensor_type")
            or doc.get("category")
            or "Unknown Incident"
        )
 
        content = (
            doc.get("content")
            or doc.get("details")
            or doc.get("description")
            or doc.get("summary")
            or doc.get("event")
            or ""
        )
 
        source_type = (
            doc.get("source_type")
            or doc.get("sensor_type")
            or doc.get("category")
            or "Unknown"
        )
 
        chunks = chunk_text(content)
 
        for i, chunk in enumerate(chunks):
 
            chunked_documents.append({
 
                "doc_id": doc.get("doc_id", "UNKNOWN"),
 
                "title": title,
 
                "source_type": source_type,
 
                "location": doc.get("location", "Unknown"),
 
                "timestamp": doc.get("timestamp", ""),
 
                "chunk_id": f"{doc.get('doc_id','DOC')}_{i}",
 
                "text": chunk
 
            })
 
    print(f"Created {len(chunked_documents)} chunks")
 
    texts = [doc["text"] for doc in chunked_documents]
 
    print("Generating embeddings...")
 
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    ).astype(np.float32)
 
    dimension = embeddings.shape[1]
 
    index = faiss.IndexFlatL2(dimension)
 
    index.add(embeddings)
 
    print(f"Knowledge Base Ready ({index.ntotal} vectors)")
    knowledge_base_name = current_dataset
 
# ==========================================
# 7. RETRIEVAL FUNCTION
# ==========================================
 
def retrieve(query, top_k=5):
 
    global index
 
    if index is None:
 
        raise ValueError(
            "Knowledge Base not loaded."
        )
 
    if not query:
 
        query = "security incident"
 
    query_embedding = model.encode(
        [str(query)],
        convert_to_numpy=True
    ).astype(np.float32)
 
    distances, indices = index.search(query_embedding, top_k)
 
    results = []
 
    for idx in indices[0]:
        if 0 <= idx < len(chunked_documents):
            results.append(chunked_documents[idx])
 
    return results
 
 
# ==========================================
# 8. CITATION SEARCH SYSTEM
# ==========================================
 
def search_with_citations(query):
 
    results = retrieve(query, top_k=5)
 
    citations = set()
 
    print("\n" + "=" * 70)
    print("INTELLIGENCE REPORT")
    print("=" * 70)
 
    for doc in results:
 
        print(f"\nDocument ID : {doc['doc_id']}")
        print(f"Title       : {doc['title']}")
        print(f"Type        : {doc['source_type']}")
        print(f"Location    : {doc['location']}")
        print(f"Timestamp   : {doc['timestamp']}")
        print(f"Content     : {doc['text']}")
 
        citations.add(doc["doc_id"])
 
    print("\n" + "=" * 70)
    print("SOURCE EVIDENCE")
    print("=" * 70)
 
    for cid in sorted(citations):
        print(cid)
 
 
# ==========================================
# 9. MAIN LOOP
# ==========================================
 
print("\nIntelligence Database Ready")
 
def retrieve_evidence(query):
 
    results = retrieve(query)
 
    return results
 
def retrieval_node(state):
 
    entities = state.get("entities", {})
    incident = state.get("incident", {})
 
    query = (
        entities.get("attack_vector")
        or incident.get("event")
        or incident.get("title")
        or incident.get("category")
        or incident.get("sensor_type")
        or incident.get("details")
        or incident.get("description")
        or "security incident"
    )
 
    print("Query Sent To Retrieval:", query)
 
    state["evidence"] = retrieve_evidence(query)
 
    return state
 