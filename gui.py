
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'  # Suppress Tk deprecation warning
import tkinter as tk
import threading
import time
from core import message_queue, log_filepath

def log_to_file(question, answer):
    with open(log_filepath, "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\nA: {answer}\n{'-'*60}\n")

class TeleprompterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interview Teleprompter")

        # Dynamically size window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = min(1200, screen_width - 100)
        height = min(500, screen_height - 200)
        
        # Configure window but don't set geometry yet
        self.root.configure(bg="black")
        self.root.attributes("-topmost", True)

        self.text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 18),
                            bg="black", fg="yellow", padx=20, pady=20)
        self.text.pack(expand=True, fill=tk.BOTH)
        
        # Force initial layout calculation
        self.root.update_idletasks()
        
        # NOW set the geometry after widgets are packed
        self.root.geometry(f"{width}x{height}+50+50")
        self.root.minsize(400, 200)

        self.check_queue()

    def calculate_optimal_size(self, content):
        """Calculate optimal window size based on content length"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Estimate content dimensions
        lines = content.split('\n')
        max_line_length = max(len(line) for line in lines) if lines else 50
        num_lines = len(lines)
        
        # Account for word wrapping - approximate characters per line based on window width
        chars_per_line = max(50, min(120, screen_width // 12))  # Rough estimate
        wrapped_lines = sum(max(1, len(line) // chars_per_line + (1 if len(line) % chars_per_line else 0)) for line in lines)
        
        # Calculate dimensions with padding
        char_width = 11  # Approximate character width for Helvetica 18
        line_height = 24  # Approximate line height for Helvetica 18
        
        content_width = min(max_line_length * char_width + 80, screen_width - 100)
        content_height = wrapped_lines * line_height + 80
        
        # Set reasonable bounds
        min_width, max_width = 400, screen_width - 100
        min_height, max_height = 200, screen_height - 100
        
        optimal_width = max(min_width, min(content_width, max_width))
        optimal_height = max(min_height, min(content_height, max_height))
        
        print(f"🔧 GUI: Calculated optimal size: {optimal_width}x{optimal_height} (lines: {wrapped_lines})")
        
        return optimal_width, optimal_height

    def update_text(self, content):
        print(f"🔧 GUI: update_text called with content length: {len(content)}")
        print(f"🔧 GUI: Content preview: {content[:200]}...")
        
        try:
            # Calculate optimal window size for this content
            optimal_width, optimal_height = self.calculate_optimal_size(content)
            
            # Clear existing text
            self.text.delete(1.0, tk.END)
            print("🔧 GUI: Text widget cleared")
            
            # Insert new content
            self.text.insert(1.0, content)  # Use 1.0 instead of tk.END
            print("🔧 GUI: New content inserted")
            
            # Force multiple update cycles
            self.text.update_idletasks()
            self.root.update_idletasks()
            
            # Resize window to fit content
            current_geometry = self.root.geometry()
            new_geometry = f"{optimal_width}x{optimal_height}+50+50"
            self.root.geometry(new_geometry)
            print(f"🔧 GUI: Resized window from {current_geometry} to {new_geometry}")
            
            # Final update cycles after resize
            self.text.update()
            self.root.update()
            print("🔧 GUI: Widget updates forced")
            
            # Check what's actually in the text widget
            current_text = self.text.get(1.0, tk.END).strip()
            print(f"🔧 GUI: Text widget now contains: {current_text[:100]}...")
            
            # Make sure window is visible and on top
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.root.attributes("-topmost", True)
            print("🔧 GUI: Window brought to front")
            
            # Scroll to top and play sound
            self.text.see(1.0)
            self.root.bell()
            print("🔧 GUI: Bell sound played and scrolled to top")
            
        except Exception as e:
            print(f"❌ GUI: Error in update_text: {e}")

    def check_queue(self):
        try:
            if not message_queue.empty():
                question, answer = message_queue.get()
                print(f"🖥️ GUI: Displaying answer for: {question[:50]}...")
                print(f"🖥️ GUI: Answer preview: {answer[:100]}...")
                self.update_text(answer)
                threading.Thread(target=log_to_file, args=(question, answer)).start()
            else:
                # Uncomment for verbose debugging
                # print("🔍 GUI: Queue is empty, checking again...")
                pass
        except Exception as e:
            print(f"❌ GUI Error in check_queue: {e}")
        self.root.after(500, self.check_queue)

def run_gui():
    print("📱 Interview Teleprompter is running...")
    root = tk.Tk()
    app = TeleprompterApp(root)
    
    # Handle window close button
    def on_closing():
        print("🛑 Window closing...")
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 GUI: Keyboard interrupt received")
        on_closing()
