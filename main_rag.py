import os 
import uuid
from pinecone import Pinecone as pine
import goggle.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# GMAIL RAG

pine.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)


index_name = "quickstart-py"
if not pine.has_index(index_name):
    pine.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )


# def embed_text(text, task="RETRIEVAL_DOCUMENT"):
#     return genai.embed_text(
#         text=text,
#         model="text-embedding-004",
#         task=task
#     )["embedding"]


#pinecone here


# # Step 1: Add 2 emails
# emails = {
#     "email1": "Hi John, just a reminder about the team meeting on Tuesday at 3pm. Let me know if you need slides.",
#     "email2": "Dear client, your subscription will expire in 3 days. Please renew to avoid service interruption."
# }

# for key, text in emails.items():
#     embedding = embed_text(text)
#     index.upsert([
#         (str(uuid.uuid4()), embedding, {"text": text, "email_id": key})
#     ])

# print("✅ Emails embedded in Pinecone.")

# # Step 2: Accept query and run RAG
# model = genai.GenerativeModel("gemini-pro")

# while True:
#     query = input("\n🔍 Ask something (or leave blank to quit): ")
#     if not query.strip():
#         break

#     query_embedding = embed_text(query, task="RETRIEVAL_QUERY")

#     results = index.query(vector=query_embedding, top_k=1, include_metadata=True)
#     context = results["matches"][0]["metadata"]["text"]
#     print(f"\n📚 Retrieved Context: {context}")

#     prompt = f"Context:\n{context}\n\nQuestion:\n{query}"
#     response = model.generate_content(prompt)
#     print(f"\n🤖 Gemini: {response.text}")