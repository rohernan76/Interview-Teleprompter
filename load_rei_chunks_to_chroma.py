import chromadb
from chromadb.config import Settings
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load API key securely
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Clear and recreate Chroma DB for REI chunks
chroma_client = chromadb.PersistentClient(path="/Users/robertohernandez-macmini-m1/Desktop/Anthropic/Claude/INTERVIEW_TELEPROMPTER/chroma_db")

# Delete existing REI collection if it exists and create new one
try:
    chroma_client.delete_collection("rei_interview_chunks")
    print("Deleted existing rei_interview_chunks collection")
except:
    print("No existing REI collection found")

collection = chroma_client.get_or_create_collection("rei_interview_chunks")

# Load the REI knowledge chunks from the REI subdirectory
rei_chunks_path = "/Users/robertohernandez-macmini-m1/Desktop/Anthropic/Claude/INTERVIEW_TELEPROMPTER/REI/rei_knowledge_chunks.txt"
with open(rei_chunks_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

chunks = []
metadatas = []
ids = []

chunk = ""
metadata = {}
id_counter = 0

for line in lines:
    line = line.strip()
    if line.startswith("{") and line.endswith("}"):
        if chunk.strip():
            chunks.append(chunk.strip())
            metadatas.append(metadata)
            ids.append(f"rei-chunk-{id_counter}")
            id_counter += 1
            chunk = ""
        metadata = json.loads(line)
    else:
        chunk += line + " "

if chunk.strip():
    chunks.append(chunk.strip())
    metadatas.append(metadata)
    ids.append(f"rei-chunk-{id_counter}")

# Generate embeddings for REI chunks
print("Generating embeddings for REI knowledge chunks...")
embeddings = []
for chunk_text in chunks:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=chunk_text
    )
    embedding = response.data[0].embedding
    embeddings.append(embedding)

# Store REI chunks in ChromaDB
print("Storing REI chunks in Chroma DB...")
collection.add(
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print(f"✅ {len(chunks)} REI-specific chunks embedded and stored successfully.")
print("🎤 Interview Teleprompter is now ready with REI knowledge base!")
print("Run 'python3 interview_teleprompter.py' to start the REI-enhanced system.")