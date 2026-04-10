from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .data_loader import load_schemes_from_csv
from .embeddings import build_faiss_index, search_faiss, load_or_build_index
from .llm import generate_response


app = FastAPI()


# ✅ ENABLE CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔥 LOAD CSV DATASET (THIS IS YOUR "DATABASE")
print("📦 Loading CSV dataset...")
schemes_db = load_schemes_from_csv("backend/data.csv")
print(f"✅ Loaded {len(schemes_db)} schemes")


# 🔥 BUILD FAISS INDEX
print("🧠 Building FAISS index...")
faiss_index = build_faiss_index(schemes_db)
print("✅ FAISS ready")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "🚀 AI Scheme Assistant Running (CSV + FAISS + LLM)"}


@app.post("/chat")
def chat(req: ChatRequest):
    user_query = req.message.strip()

    print("\n==============================")
    print("👤 USER QUERY:", user_query)

    # ❌ Empty input
    if not user_query:
        return {"response": "Please enter a valid question."}

    # 🔍 FAISS SEARCH (THIS IS YOUR DATABASE QUERY)
    results = search_faiss(user_query, faiss_index, schemes_db)

    print("🔎 MATCHED SCHEMES:", len(results))

    if not results:
        return {"response": "Sorry, I couldn't find a relevant scheme."}

    responses = []

    for i, scheme in enumerate(results):
        print(f"➡️ Result {i+1}: {scheme.get('scheme_name')}")

        try:
            res = generate_response(user_query, scheme)
        except Exception as e:
            print("❌ LLM ERROR:", e)
            res = f"Error generating response for {scheme.get('scheme_name','')}"

        responses.append(res)

    # 🔥 Combine responses
    final_response = "\n\n----------------------\n\n".join(responses)

    return {"response": final_response}