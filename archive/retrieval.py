import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ==========================================
# 1. LOAD DATASET (DOCUMENT INGESTION)
# ==========================================

try:
    with open("cyber_incidents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)

    print(f"Loaded {len(documents)} documents")

except Exception as e:
    print("Error loading data:", e)
    exit()


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
# 3. PREPARE CHUNKED DOCUMENTS
# ==========================================

chunked_documents = []

for doc in documents:

    title = doc.get("title", doc.get("event", "No Title"))
    content = doc.get("content", doc.get("details", ""))
    source_type = doc.get("source_type", doc.get("sensor_type", "unknown"))

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


# ==========================================
# 4. LOAD EMBEDDING MODEL (ONLY ONCE)
# ==========================================

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully")


# ==========================================
# 5. GENERATE EMBEDDINGS
# ==========================================

texts = [doc["text"] for doc in chunked_documents]

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

embeddings = embeddings.astype(np.float32)

print(f"Generated {len(embeddings)} embeddings")


# ==========================================
# 6. CREATE FAISS INDEX
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"FAISS index contains {index.ntotal} vectors")


# ==========================================
# 7. RETRIEVAL FUNCTION
# ==========================================

def retrieve(query, top_k=5):

    query_embedding = model.encode(
        [query],
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

while True:

    query = input("\nEnter Query (or type 'exit'): ").strip()

    if query.lower() == "exit":
        print("Exiting...")
        break

    if not query:
        print("Please enter a valid query.")
        continue

    search_with_citations(query)