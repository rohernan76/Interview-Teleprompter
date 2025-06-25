"""Diagnostic version of the main entry point"""

import signal
import sys
from core import start_file_monitor
from gui_diagnostic import run_diagnostic_gui

def signal_handler(sig, frame):
    print("\n🛑 DIAGNOSTIC: Shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    print("🔍 STARTING DIAGNOSTIC MODE")
    print("="*50)
    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    observer = start_file_monitor()
    try:
        run_diagnostic_gui()
    except KeyboardInterrupt:
        print("\n🛑 DIAGNOSTIC: Keyboard interrupt received")
    finally:
        observer.stop()
        observer.join()
        print("📴 DIAGNOSTIC: File monitor stopped")