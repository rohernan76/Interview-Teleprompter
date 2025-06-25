
import os
import time
from queue import Queue
from dotenv import load_dotenv
import openai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Load environment variables and set API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Thread-safe message queue
message_queue = Queue()

# Custom log path
log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
log_filepath = os.path.join(
    "/Users/robertohernandez_macpro2020/Desktop/ResumeRocket/Interview-Teleprompter/Interview Logs/",
    log_filename
)

# Memory for context-aware answers
last_question = None
last_answer = None

def ask_gpt(question):
    global last_question, last_answer

    with open("prep_notes_hadanou_summary.txt", "r", encoding="utf-8") as f:
        prep_notes = f.read()

    messages = [
        {"role": "system", "content": prep_notes}
    ]

    if last_question and last_answer:
        messages.append({"role": "user", "content": f"Previous Q: {last_question}\nPrevious A: {last_answer}"})

    messages.append({"role": "user", "content": f"Question: {question}"})

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=0.6,
        max_tokens=500,
    )

    answer = response.choices[0].message.content.strip()
    last_question = question
    last_answer = answer
    return answer

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
