
import tkinter as tk
import threading
import time
from core import message_queue, log_filepath

# Set up logging file for Q + A
log_file = "interview_log.txt"

def show_answer_window(question, answer):
    def log_to_file():
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"Q: {question}\n")
            f.write(f"A: {answer}\n")
            f.write("-" * 50 + "\n")

    def display():
        root = tk.Tk()
        root.title("Interview Teleprompter")

        # Dynamically calculate size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        width = min(1200, screen_width - 100)
        height = min(300, screen_height - 200)

        root.geometry(f"{width}x{height}+50+50")
        root.configure(bg="black")

        text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 20), bg="black", fg="yellow", padx=20, pady=20)
        text.insert(tk.END, answer)
        text.pack(expand=True, fill=tk.BOTH)

        root.attributes("-topmost", True)
        root.mainloop()

    threading.Thread(target=log_to_file).start()
    threading.Thread(target=display).start()

def run_gui():
    print("📱 Interview Teleprompter is running...")
    while True:
        if not message_queue.empty():
            question, answer = message_queue.get()
            show_answer_window(question, answer)
        time.sleep(0.5)
