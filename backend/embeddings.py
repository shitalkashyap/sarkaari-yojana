from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "backend/faiss.index"


def build_faiss_index(schemes):
    texts = []

    for scheme in schemes:
        text = " ".join([
            scheme.get("scheme_name", ""),
            scheme.get("description", ""),
            scheme.get("benefits", ""),
            scheme.get("eligibility", ""),
            scheme.get("category", ""),
            scheme.get("tags", "")
        ])
        texts.append(text)

    print(f"🧠 Generating embeddings for {len(texts)} schemes...")

    batch_size = 64
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]

        emb = model.encode(batch)
        all_embeddings.append(emb)

        print(f"⚡ {i + len(batch)} / {len(texts)}")

    embeddings = np.vstack(all_embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # ✅ SAVE INDEX
    faiss.write_index(index, INDEX_PATH)
    print("💾 FAISS index saved")

    return index


def load_or_build_index(schemes):
    if os.path.exists(INDEX_PATH):
        print("⚡ Loading FAISS index from disk...")
        return faiss.read_index(INDEX_PATH)

    print("❌ No index found. Building new one...")
    return build_faiss_index(schemes)


def search_faiss(query, index, schemes, k=3):
    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), k)

    results = []
    for idx in indices[0]:
        if idx < len(schemes):
            results.append(schemes[idx])

    return results