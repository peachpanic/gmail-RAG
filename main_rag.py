import os 
import uuid
from pinecone import Pinecone 
import google.generativeai as genai
from dotenv import load_dotenv
from simplegmail import Gmail
from simplegmail.query import construct_query

load_dotenv()

# Configure APIs
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Initialize Gmail
gmail = Gmail()

# Setup Pinecone index
index_name = "gmail-rag-index"
if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "text"} 
        }
    )

index = pc.Index(index_name)


def format_messages(message):
    # need to format message content dfso i can chunk it
    print("yo mama")

def fetch_and_upsert_emails():
    
    query_params = {
        "newer_than": "5d",  
        "unread": True,   
    }
    
    messages = gmail.get_messages(query=construct_query(query_params))
    
    email_records = []
    
    for message in messages:
        print("This is the message: ", message)
        email_content = f"""
        Body: {message.plain or message.snippet or 'No content'}
        """
        record = {
            "_id": f"email_{message.id}",
            "text": email_content.strip(),
            "subject": message.subject or 'No Subject',
            "sender": message.sender or 'Unknown Sender',
            "date": str(message.date) if message.date else 'Unknown Date',
            "message_id": message.id,
        }
        print(f"Snippet: {message.snippet}")
        email_records.append(record)
        

    if email_records:
        print(f"🔄 Upserting {len(email_records)} emails to Pinecone...")

        batch_size = 5
        for i in range(0, len(email_records), batch_size):
            batch = email_records[i:i + batch_size]
            index.upsert_records("gmail-namespace", batch)
            print(f"✅ Upserted batch {i//batch_size + 1}")
        
        print(f"✅ All {len(email_records)} emails embedded in Pinecone!")
    else:
        print("❌ No emails found to upsert.")
    
    return len(email_records)

def query_emails(user_query):
    """Query emails using RAG"""
    try:

        query_embedding = genai.embed_content(
            model="models/embedding-001",
            content=user_query,
            task_type="RETRIEVAL_QUERY"
        )["embedding"]
        

        results = index.query(
            vector=query_embedding,
            top_k=5,
            include_metadata=True,
            namespace="gmail-namespace"
        )
        
        if results["matches"]:
            contexts = []
            for match in results["matches"]:
                contexts.append({
                    "text": match["metadata"]["text"],
                    "subject": match["metadata"]["subject"],
                    "sender": match["metadata"]["sender"],
                    "score": match["score"]
                })
            
            return contexts
        else:
            return []
            
    except Exception as e:
        print(f"❌ Query error: {e}")
        return []

if __name__ == "__main__":

    email_count = fetch_and_upsert_emails()
    
    if email_count > 0:
        print(f"✅ Successfully processed {email_count} emails.")
