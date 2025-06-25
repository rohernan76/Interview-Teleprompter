
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load API key securely
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Clear and recreate Chroma DB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_client.delete_collection("interview_chunks")
collection = chroma_client.get_or_create_collection("interview_chunks")

# Load the new, complete chunk set
with open("knowledge_chunks_complete.txt", "r", encoding="utf-8") as f:
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
            ids.append(f"chunk-{id_counter}")
            id_counter += 1
            chunk = ""
        metadata = json.loads(line)
    else:
        chunk += line + " "

if chunk.strip():
    chunks.append(chunk.strip())
    metadatas.append(metadata)
    ids.append(f"chunk-{id_counter}")

# Generate embeddings
print("Generating embeddings for new full chunk set...")
embeddings = []
for chunk_text in chunks:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=chunk_text
    )
    embedding = response.data[0].embedding
    embeddings.append(embedding)

# Store new chunks
print("Storing new chunks in Chroma DB...")
collection.add(
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print(f"✅ {len(chunks)} updated chunks embedded and stored successfully.")
