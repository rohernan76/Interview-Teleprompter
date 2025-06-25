"""Entry point for Interview Teleprompter application."""

import signal
import sys
from core import start_file_monitor
from gui import run_gui

def signal_handler(sig, frame):
    print("\n🛑 Shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    observer = start_file_monitor()
    try:
        run_gui()
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received")
    finally:
        observer.stop()
        observer.join()
        print("📴 File monitor stopped")
