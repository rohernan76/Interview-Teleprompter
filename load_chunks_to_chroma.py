
import chromadb
from openai import OpenAI
import os
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Chroma client (local)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(name="interview_chunks")

# Load the chunked data
with open("knowledge_chunks_revised.txt", "r", encoding="utf-8") as f:
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
        # Save previous chunk
        if chunk.strip():
            chunks.append(chunk.strip())
            metadatas.append(metadata)
            ids.append(f"chunk-{id_counter}")
            id_counter += 1
            chunk = ""
        metadata = json.loads(line)
    else:
        chunk += line + " "

# Add the final chunk
if chunk.strip():
    chunks.append(chunk.strip())
    metadatas.append(metadata)
    ids.append(f"chunk-{id_counter}")

# Generate embeddings
print("Generating embeddings...")
embeddings = []
for chunk_text in chunks:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=chunk_text
    )
    embedding = response.data[0].embedding
    embeddings.append(embedding)

# Add to Chroma
print("Storing chunks in Chroma DB...")
collection.add(
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print(f"✅ {len(chunks)} chunks embedded and stored successfully.")
