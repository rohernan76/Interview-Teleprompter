
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variable
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load Chroma DB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("interview_chunks")

# Local memory
last_question = None
last_answer = None
cached_chunks = None

def is_followup(query):
    follow_ups = ["can you", "what about", "how so", "can i clarify", "elaborate", "tell me more", "follow up"]
    return any(query.lower().startswith(phrase) for phrase in follow_ups)

while True:
    try:
        question = input("\n🔍 Enter your interview question (or type 'exit' to quit): ").strip()
        if question.lower() == "exit":
            break

        context = ""

        if is_followup(question) and last_question and last_answer and cached_chunks:
            print("🔁 Detected follow-up. Reusing previous context.")
            context = "\n\n".join(cached_chunks) + f"\n\nPrevious Q: {last_question}\nPrevious A: {last_answer}"
        else:
            # Embed question
            response = client.embeddings.create(
                model="text-embedding-ada-002",
                input=question
            )
            query_embedding = response.data[0].embedding

            # Query Chroma
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3,
                include=["documents"]
            )
            cached_chunks = results["documents"][0]
            context = "\n\n".join(cached_chunks)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are Roberto Hernández’s AI interview assistant. "
                    "Generate clear, confident, first-person answers that reflect Roberto’s voice, values, and experience."
                )
            },
            {"role": "user", "content": f"Relevant background:{context}"},
            {"role": "user", "content": f"Interview question: {question}"},
        ]

        answer = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.6,
            max_tokens=500
        )

        reply = answer.choices[0].message.content.strip()
        print("\n🧠 GPT-4 Response:")
        print(reply)

        last_question = question
        last_answer = reply

    except KeyboardInterrupt:
        print("\n👋 Session ended.")
        break
