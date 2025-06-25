import tkinter as tk
import threading
import time
from core import message_queue, log_filepath

# Set up logging file for Q + A
log_file = "interview_log.txt"

def log_to_file(question, answer):
    """Log the Q&A to a file in a separate thread"""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\n")
        f.write(f"A: {answer}\n")
        f.write("-" * 50 + "\n")

class TeleprompterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interview Teleprompter")
        
        # Dynamically calculate size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        width = min(1200, screen_width - 100)
        height = min(300, screen_height - 200)
        
        self.root.geometry(f"{width}x{height}+50+50")
        self.root.configure(bg="black")
        
        self.text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 20), 
                            bg="black", fg="yellow", padx=20, pady=20)
        self.text.pack(expand=True, fill=tk.BOTH)
        
        self.root.attributes("-topmost", True)
        
        # Start checking for messages
        self.check_message_queue()
    
    def update_text(self, answer):
        """Update the text widget with a new answer"""
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, answer)
    
    def check_message_queue(self):
        """Check for new messages every 500ms"""
        if not message_queue.empty():
            question, answer = message_queue.get()
            self.update_text(answer)
            
            # Log in a separate thread to avoid blocking the UI
            threading.Thread(
                target=log_to_file, 
                args=(question, answer)
            ).start()
        
        # Schedule the next check
        self.root.after(500, self.check_message_queue)

def run_gui():
    print("📱 Interview Teleprompter is running...")
    root = tk.Tk()
    app = TeleprompterApp(root)
    root.mainloop()
