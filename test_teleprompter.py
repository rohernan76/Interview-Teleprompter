#!/usr/bin/env python3
"""
Simple test script to verify teleprompter functionality
"""

import time
import os

def test_file_append():
    """Test by appending a question to whisper_output.txt"""
    test_question = "What is your greatest strength?"
    
    print("🧪 Testing teleprompter by adding a test question...")
    print(f"📝 Question: {test_question}")
    
    # Append to whisper_output.txt
    with open("whisper_output.txt", "a") as f:
        f.write(f"\n{test_question}\n")
    
    print("✅ Test question added to whisper_output.txt")
    print("👀 Check if the GUI displays a response...")

def monitor_logs():
    """Monitor the latest log file"""
    log_dir = "Interview Logs"
    if not os.path.exists(log_dir):
        print("❌ No Interview Logs directory found")
        return
    
    log_files = [f for f in os.listdir(log_dir) if f.startswith("log_")]
    if not log_files:
        print("❌ No log files found")
        return
    
    latest_log = max(log_files)
    log_path = os.path.join(log_dir, latest_log)
    
    print(f"📖 Monitoring latest log: {latest_log}")
    
    # Read and display the log
    try:
        with open(log_path, "r") as f:
            content = f.read()
            if content.strip():
                print("📄 Latest log content:")
                print("-" * 50)
                print(content)
                print("-" * 50)
            else:
                print("📭 Log file is empty")
    except Exception as e:
        print(f"❌ Error reading log: {e}")

if __name__ == "__main__":
    print("🧪 Teleprompter Test Utility")
    print("1. Add test question")
    print("2. Monitor logs")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        test_file_append()
    elif choice == "2":
        monitor_logs()
    else:
        print("❌ Invalid choice")
