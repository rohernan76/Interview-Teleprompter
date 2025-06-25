import os
import time
import tkinter as tk
from queue import Queue
from dotenv import load_dotenv
import openai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load interview prep notes
with open("prep_notes.txt", "r", encoding="utf-8") as f:
    prep_notes = f.read()

# System message to guide AI responses
system_prompt = (
    "You are my real-time AI interview assistant. I am currently in a live job interview. "
    "When I give you a question (transcribed from the interviewer), your job is to generate a concise, professional, and confident answer that sounds like me. "
    "Use my interview prep materials (resume, job description, success stories, etc.) to craft answers that align with the role and showcase my strengths. "
    "Keep answers brief but specific. Do not restate the question. Speak in the first person. Prioritize clarity, calm confidence, and professionalism. Use a warm tone but remain sharp and direct."
)

# Logging setup
log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
log_filepath = os.path.join(os.getcwd(), log_filename)

# Teleprompter display cooldown
last_display_time = 0
cooldown_seconds = 3

# Thread-safe queue
message_queue = Queue()

def ask_gpt(question):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Here is my interview prep:\n{prep_notes}"},
        {"role": "user", "content": f"Question: {question}"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.6,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

class WhisperOutputHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_question = None
        self.last_time = 0
        self.cooldown = 5  # seconds

    def on_modified(self, event):
        if event.src_path.endswith("whisper_output.txt"):
            try:
                with open(event.src_path, "r") as f:
                    lines = f.readlines()
                if lines:
                    latest = lines[-1].strip()
                    now = time.time()
                    if (
                        latest and
                        latest != self.last_question and
                        now - self.last_time > self.cooldown
                    ):
                        self.last_question = latest
                        self.last_time = now
                        print(f"New question: {latest}")
                        try:
                            answer = ask_gpt(latest)
                            message_queue.put((latest, answer))
                        except Exception as e:
                            print(f"Error generating response: {e}")
            except Exception as e:
                print(f"Failed to read whisper_output.txt: {e}")

def show_answer_window(root, answer):
    popup = tk.Toplevel(root)
    popup.title("Interview Teleprompter")
    popup.geometry("820x220+100+100")
    popup.configure(bg="black")

    label = tk.Label(
        popup,
        text=answer,
        wraplength=780,
        justify="left",
        font=("Helvetica", 16),
        anchor="w",
        padx=20,
        pady=20,
        bg="black",
        fg="lime"
    )
    label.pack(fill="both", expand=True)
    popup.attributes('-topmost', True)
    popup.after(25000, popup.destroy)

def poll_queue(root):
    try:
        while not message_queue.empty():
            question, answer = message_queue.get()
            show_answer_window(root, answer)

            # Append to log
            with open(log_filepath, "a", encoding="utf-8") as log_file:
                timestamp = datetime.now().strftime('%H:%M:%S')
                log_file.write(f"\n[{timestamp}] QUESTION: {question}\n")
                log_file.write(f"[{timestamp}] ANSWER: {answer}\n")
    except Exception as e:
        print(f"❌ Error in queue processing: {e}")
    finally:
        root.after(500, lambda: poll_queue(root))  # Poll again soon

def start_gui():
    root = tk.Tk()
    root.withdraw()  # Hide main window
    root.after(100, lambda: poll_queue(root))
    print("📱 Interview Teleprompter is running...")
    root.mainloop()

def start_file_monitor():
    observer = Observer()
    observer.schedule(WhisperOutputHandler(), path=os.getcwd(), recursive=False)
    observer.start()
    return observer

if __name__ == "__main__":
    observer = start_file_monitor()
    try:
        start_gui()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
