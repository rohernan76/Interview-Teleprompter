
import tkinter as tk
import threading
import time
from core import message_queue

# Logging path
log_file = "/Users/robertohernandez_macpro2020/Desktop/ResumeRocket/Interview-Teleprompter/Interview Logs/interview_log.txt"

def log_to_file(question, answer):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\n")
        f.write(f"A: {answer}\n")
        f.write("-" * 50 + "\n")

class TeleprompterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interview Teleprompter")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = min(1200, screen_width - 100)

        self.root.geometry(f"{width}x300+50+50")
        self.root.configure(bg="black")

        self.text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 20),
                            bg="black", fg="yellow", padx=20, pady=20, bd=0)
        self.text.pack(expand=True, fill=tk.BOTH)

        self.root.attributes("-topmost", True)
        self.check_message_queue()

    def update_text(self, answer):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, answer)
        self.text.update_idletasks()

        # Estimate new height based on rendered line height
        font_metrics = self.text.dlineinfo("1.0")
        line_height = font_metrics[3] if font_metrics else 30
        total_lines = int(self.text.index('end-1c').split('.')[0])
        new_height = min((line_height * total_lines) + 100, self.root.winfo_screenheight() - 80)

        self.root.geometry(f"{self.root.winfo_width()}x{new_height}")

    def check_message_queue(self):
        if not message_queue.empty():
            question, answer = message_queue.get()
            self.update_text(answer)
            threading.Thread(target=log_to_file, args=(question, answer)).start()

        self.root.after(500, self.check_message_queue)

def run_gui():
    print("📱 Interview Teleprompter is running...")
    root = tk.Tk()
    app = TeleprompterApp(root)
    root.mainloop()
