import requests
import json

HF_API_KEY = "YOUR_HF_API_KEY"

MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


# 🔥 CALL LLM
def query_llm(prompt):
    try:
        response = requests.post(
            MODEL_URL,
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.3
                }
            },
            timeout=12
        )

        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "")

        return ""

    except Exception as e:
        print("LLM ERROR:", e)
        return ""


# 🔥 MAIN RESPONSE GENERATOR
def generate_response(user_query, scheme):
    prompt = f"""
You are a helpful Indian government schemes assistant.

TASK:
1. Detect the language of the user query.
2. Respond in the SAME language (Hindi, Hinglish, English, etc.).
3. Explain in VERY SIMPLE language (like explaining to a common person).
4. Avoid complex words. Use short sentences.

USER QUERY:
{user_query}

SCHEME DATA:
{json.dumps(scheme)}

RESPONSE FORMAT (STRICT):

📌 Scheme Name:
🏛 Ministry:
🎯 Who can benefit:
✅ Eligibility:
💰 Benefits:
📄 Documents:
📝 How to apply:

IMPORTANT:
- Keep language simple
- Use bullet points if possible
- Translate if needed
"""

    output = query_llm(prompt)

    # ✅ fallback if LLM fails
    if not output:
        return basic_format(scheme)

    return output


# 🔥 FALLBACK (NO LLM)
def basic_format(scheme):
    return f"""
📌 Scheme Name: {scheme.get('scheme_name', '')}

🏛 Ministry: {scheme.get('ministry', '')}

🎯 Category:
{scheme.get('category', '')}

✅ Eligibility:
{scheme.get('eligibility', '')}

💰 Benefits:
{scheme.get('benefits', '')}

📄 Documents:
{scheme.get('documents', '')}

📝 How to apply:
{scheme.get('application_process', '')}
"""  