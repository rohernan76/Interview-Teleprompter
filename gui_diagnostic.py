import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import tkinter as tk
import threading
import time
from core import message_queue, log_filepath

def log_to_file(question, answer):
    with open(log_filepath, "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\nA: {answer}\n{'-'*60}\n")

class DiagnosticTeleprompterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interview Teleprompter - DIAGNOSTIC")
        
        # Force window size and position
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = min(1200, screen_width - 100)
        height = min(500, screen_height - 200)
        
        print(f"🔍 DIAG: Screen size: {screen_width}x{screen_height}")
        print(f"🔍 DIAG: Window size: {width}x{height}")
        
        # DON'T set geometry yet - let widgets size first
        self.root.configure(bg="red")  # Changed to red to verify background
        self.root.attributes("-topmost", True)
        
        # Create and configure text widget with maximum visibility
        print("🔍 DIAG: Creating text widget...")
        self.text = tk.Text(
            root, 
            wrap=tk.WORD, 
            font=("Courier", 24),  # Changed to Courier, larger size
            bg="white",            # Changed to white background
            fg="black",            # Changed to black text
            padx=20, 
            pady=20,
            relief=tk.RAISED,      # Added border
            bd=5,                  # Border width
            insertbackground="red" # Cursor color
        )
        
        print("🔍 DIAG: Packing text widget...")
        self.text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Force initial layout calculation
        self.root.update_idletasks()
        
        # NOW set the geometry after widgets are laid out
        print(f"🔍 DIAG: Setting geometry to {width}x{height}+50+50")
        self.root.geometry(f"{width}x{height}+50+50")
        self.root.minsize(400, 200)  # Set minimum size
        
        # Insert test content immediately
        test_content = "DIAGNOSTIC MODE - If you can see this, the widget works!\n\nWaiting for real content..."
        self.text.insert("1.0", test_content)
        
        print("🔍 DIAG: Text widget setup complete")
        self.debug_widget_state()
        
        # Force immediate display
        self.root.update()
        self.root.update_idletasks()
        
        self.check_queue()

    def debug_widget_state(self):
        """Comprehensive widget diagnostics"""
        print("\n" + "="*50)
        print("🔍 COMPREHENSIVE WIDGET DIAGNOSTICS")
        print("="*50)
        
        try:
            # Basic widget info
            print(f"Widget exists: {self.root.winfo_exists()}")
            print(f"Widget mapped: {self.text.winfo_ismapped()}")
            print(f"Widget viewable: {self.text.winfo_viewable()}")
            print(f"Widget width: {self.text.winfo_width()}")
            print(f"Widget height: {self.text.winfo_height()}")
            print(f"Widget x: {self.text.winfo_x()}")
            print(f"Widget y: {self.text.winfo_y()}")
            
            # Text content
            content = self.text.get("1.0", tk.END)
            print(f"Content length: {len(content)}")
            print(f"Content preview: '{content[:100]}'")
            print(f"Content repr: {repr(content[:50])}")
            
            # Widget configuration
            print(f"Background: {self.text.cget('bg')}")
            print(f"Foreground: {self.text.cget('fg')}")
            print(f"Font: {self.text.cget('font')}")
            print(f"State: {self.text.cget('state')}")
            print(f"Relief: {self.text.cget('relief')}")
            print(f"Border width: {self.text.cget('bd')}")
            
            # Window info
            print(f"Window geometry: {self.root.geometry()}")
            print(f"Window state: {self.root.state()}")
            print(f"Window focus: {self.root.focus_get()}")
            
        except Exception as e:
            print(f"❌ DIAG: Error in diagnostics: {e}")
            import traceback
            traceback.print_exc()
        
        print("="*50 + "\n")

    def update_text(self, content):
        print(f"\n🔧 DIAG: update_text called with {len(content)} chars")
        print(f"🔧 DIAG: Content preview: '{content[:100]}'")
        
        def _safe_update():
            print("🔧 DIAG: _safe_update executing...")
            try:
                # Pre-update diagnostics
                print("🔧 DIAG: Pre-update state:")
                self.debug_widget_state()
                
                # Clear and insert
                print("🔧 DIAG: Clearing text...")
                self.text.delete("1.0", tk.END)
                
                print("🔧 DIAG: Inserting new content...")
                self.text.insert("1.0", content)
                
                # Force multiple refresh attempts
                print("🔧 DIAG: Forcing updates...")
                self.text.update()
                self.text.update_idletasks()
                self.root.update()
                self.root.update_idletasks()
                
                # Post-update diagnostics
                print("🔧 DIAG: Post-update state:")
                self.debug_widget_state()
                
                # Window management
                print("🔧 DIAG: Managing window...")
                self.root.deiconify()
                self.root.lift()
                self.root.focus_force()
                self.root.bell()
                
                print("🔧 DIAG: Update completed successfully")
                
            except Exception as e:
                print(f"❌ DIAG: Error in _safe_update: {e}")
                import traceback
                traceback.print_exc()
        
        print("🔧 DIAG: Scheduling _safe_update...")
        self.root.after(0, _safe_update)

    def check_queue(self):
        print("🔍 DIAG: Checking queue...")
        try:
            processed = 0
            while not message_queue.empty():
                try:
                    question, answer = message_queue.get_nowait()
                    processed += 1
                    print(f"🖥️ DIAG: Processing message #{processed}")
                    print(f"🖥️ DIAG: Question: {question[:50]}...")
                    print(f"🖥️ DIAG: Answer length: {len(answer)}")
                    
                    self.update_text(answer)
                    threading.Thread(target=log_to_file, args=(question, answer), daemon=True).start()
                    
                    # Only process one message at a time for debugging
                    break
                    
                except Exception as e:
                    print(f"❌ DIAG: Error processing queue item: {e}")
                    break
            
            if processed == 0:
                print("🔍 DIAG: Queue empty")
            
        except Exception as e:
            print(f"❌ DIAG: Queue check error: {e}")
        
        # Schedule next check
        self.root.after(1000, self.check_queue)  # Slower for debugging

def run_diagnostic_gui():
    print("📱 DIAGNOSTIC GUI Starting...")
    root = tk.Tk()
    app = DiagnosticTeleprompterApp(root)
    
    def on_closing():
        print("🛑 DIAGNOSTIC: Window closing...")
        app.debug_widget_state()
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Add manual test button
    def manual_test():
        print("🧪 MANUAL TEST: Injecting test content...")
        test_content = f"MANUAL TEST CONTENT\nTime: {time.strftime('%H:%M:%S')}\n\nThis is a test to verify the text widget updates correctly."
        app.update_text(test_content)
    
    test_button = tk.Button(root, text="MANUAL TEST", command=manual_test, 
                           bg="yellow", fg="black", font=("Arial", 14))
    test_button.pack(side=tk.BOTTOM, pady=10)
    
    try:
        print("📱 DIAGNOSTIC: Starting mainloop...")
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 DIAGNOSTIC: Keyboard interrupt")
        on_closing()
    except Exception as e:
        print(f"❌ DIAGNOSTIC: Mainloop error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_diagnostic_gui()