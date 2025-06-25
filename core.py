
import os
import time
import warnings
from queue import Queue
from dotenv import load_dotenv

# Suppress urllib3 SSL warning (harmless on macOS)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import chromadb
from openai import OpenAI

# Load environment variables and OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chroma DB setup for REI-specific interview
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("rei_interview_chunks")

# Log file setup
log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
log_filepath = os.path.join(os.getcwd(), "Interview Logs", log_filename)

# Message queue
message_queue = Queue()

# Memory store
last_question = None
last_answer = None
cached_chunks = None

def is_followup(query):
    follow_ups = ["can you", "what about", "how so", "can i clarify", "elaborate", "tell me more", "follow up"]
    return any(query.lower().startswith(phrase) for phrase in follow_ups)

def ask_gpt(question):
    global last_question, last_answer, cached_chunks
    
    print(f"🤖 ask_gpt called with question: {question}")

    try:
        if is_followup(question) and last_question and last_answer and cached_chunks:
            context = "\n\n".join(cached_chunks) + f"\n\nPrevious Q: {last_question}\nPrevious A: {last_answer}"
            print("🔄 Using cached context for follow-up question")
        else:
            print("🔍 Generating new embedding and retrieving chunks...")
            # Embed and retrieve top chunks
            embedding = client.embeddings.create(model="text-embedding-ada-002", input=question).data[0].embedding
            results = collection.query(query_embeddings=[embedding], n_results=3, include=["documents"])
            cached_chunks = results["documents"][0]
            context = "\n\n".join(cached_chunks)
            print(f"📚 Retrieved {len(cached_chunks)} chunks for context")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are Roberto Hernández's AI interview assistant for an REI Store Sales Specialist position. "
                    "Generate clear, confident, first-person answers that reflect Roberto's voice, outdoor passion, "
                    "retail experience, and alignment with REI's cooperative values. Keep responses warm, "
                    "concise, and authentic to REI's outdoor culture."
                )
            },
            {"role": "user", "content": f"Relevant background:\n{context}"},
            {"role": "user", "content": f"Interview question: {question}"}
        ]

        print("🤖 Calling OpenAI API...")
        reply = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated to current model
            messages=messages,
            temperature=0.6,
            max_tokens=500
        ).choices[0].message.content.strip()

        print(f"✅ Generated reply: {reply[:100]}...")
        
        last_question = question
        last_answer = reply

        # Save to log
        print(f"💾 Saving to log: {log_filepath}")
        os.makedirs(os.path.dirname(log_filepath), exist_ok=True)
        with open(log_filepath, "a", encoding="utf-8") as f:
            f.write(f"Q: {question}\nA: {reply}\n{'-'*60}\n")

        return reply
        
    except Exception as e:
        error_msg = f"❌ Error in ask_gpt: {e}"
        print(error_msg)
        return f"Sorry, I encountered an error processing your question: {str(e)}"

class WhisperOutputHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_question = None
        self.last_time = 0
        self.cooldown = 2
        self.seen_questions = set()

    def on_modified(self, event):
        if event.src_path.endswith("whisper_output.txt"):
            try:
                with open(event.src_path, "r") as f:
                    lines = f.readlines()
                if lines:
                    latest = next((line.strip() for line in reversed(lines) if line.strip()), "")
                    print(f"📝 Detected new line: {latest}")
                    print(f"[{time.strftime('%H:%M:%S')}] Detected new line: {latest}")
                    now = time.time()
                    if latest and now - self.last_time > self.cooldown and latest not in self.seen_questions:
                        self.last_question = latest
                        self.last_time = now
                        self.seen_questions.add(latest)
                        print(f"🧠 New question: {latest}")
                        try:
                            answer = ask_gpt(latest)
                            message_queue.put((latest, answer))
                        except Exception as e:
                            print(f"❌ Error generating response: {e}")
                    else:
                        print(f"⚠️ Skipping duplicate or recent question: {latest}")
            except Exception as e:
                print(f"❌ Failed to read whisper_output.txt: {e}")

def start_file_monitor():
    observer = Observer()
    observer.schedule(WhisperOutputHandler(), path=os.getcwd(), recursive=False)
    observer.start()
    print("📡 File monitor is now watching 'whisper_output.txt'...")
    return observer

