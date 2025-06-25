import os
import time
import threading
import tkinter as tk
from queue import Queue
from dotenv import load_dotenv
import openai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load interview prep notes
with open("prep_notes.txt", "r") as f:
    prep_notes = f.read()

system_prompt = (
    "You are my real-time AI interview assistant. I am currently in a live job interview. "
    "When I give you a question (transcribed from the interviewer), your job is to generate a concise, professional, and confident answer that sounds like me. "
    "Use my interview prep materials (resume, job description, success stories, etc.) to craft answers that align with the role and showcase my strengths. "
    "Keep answers brief but specific. Do not restate the question. Speak in the first person. Prioritize clarity, calm confidence, and professionalism. Use a warm tone but remain sharp and direct."
)

# Thread-safe message passing
message_queue = Queue()

# Debounce logic
last_question = ""
last_trigger_time = 0
COOLDOWN_SECONDS = 10

# Main Tkinter root (must be initialized in main thread)
root = tk.Tk()
root.withdraw()  # Hide root window

def ask_gpt(prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Here is my interview prep:\n{prep_notes}"},
        {"role": "user", "content": f"Question: {prompt}"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.6,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

def show_answer_window(answer):
    popup = tk.Toplevel(root)
    popup.title("Interview Teleprompter")
    popup.geometry("800x200+100+100")

    label = tk.Label(
        popup,
        text=answer,
        wraplength=740,
        justify="left",
        font=("Helvetica", 16),
        anchor="w",
        padx=20,
        pady=20
    )
    label.pack(fill="both", expand=True)
    popup.attributes('-topmost', True)
    popup.after(25000, popup.destroy)

def poll_queue():
    try:
        while not message_queue.empty():
            msg = message_queue.get()
            show_answer_window(msg)
    finally:
        root.after(500, poll_queue)

class WhisperOutputHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global last_question, last_trigger_time

        if event.src_path.endswith("whisper_output.txt"):
            try:
                with open(event.src_path, "r") as f:
                    lines = f.readlines()
                    if lines:
                        latest = lines[-1].strip()
                        now = time.time()
                        if latest and latest != last_question and now - last_trigger_time > COOLDOWN_SECONDS:
                            print(f"New question: {latest}")
                            last_question = latest
                            last_trigger_time = now
                            try:
                                answer = ask_gpt(latest)
                                message_queue.put(answer)
                            except Exception as e:
                                print(f"❌ GPT Error: {e}")
            except Exception as e:
                print(f"❌ File Read Error: {e}")

def monitor_file():
    print("📱 Interview Teleprompter is running...")
    event_handler = WhisperOutputHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.getcwd(), recursive=False)
    observer.start()
    try:
        root.after(500, poll_queue)
        root.mainloop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_file()