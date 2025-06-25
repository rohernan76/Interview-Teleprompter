
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

# Get user input
query = input("🔍 Enter your interview question: ")

# Embed the query
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=query
)
query_embedding = response.data[0].embedding

# Retrieve top 3 results
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "metadatas"]
)

# Display results
print("\n📌 Top Retrieved Chunks:")
for i in range(len(results["documents"][0])):
    print(f"\n--- Chunk #{i+1} ---")
    print(f"Source: {results['metadatas'][0][i].get('source', 'N/A')} | Category: {results['metadatas'][0][i].get('category', 'N/A')}")
    print(results["documents"][0][i])
