#!/usr/bin/env python3
"""Direct GUI test - bypasses file monitoring entirely"""

import os
import sys
sys.path.append(os.getcwd())

from core import message_queue
import time

def inject_test_content():
    """Inject test content directly into the message queue"""
    test_cases = [
        ("Test Question 1", "This is a test answer that should appear in the GUI window. If you can see this text, the basic update mechanism is working."),
        ("What is your biggest strength?", "My biggest strength is my ability to adapt quickly to new technologies and challenges. Throughout my career, I've consistently demonstrated the ability to learn new programming languages, frameworks, and methodologies as needed. For example, when I transitioned from backend development to full-stack work, I quickly mastered React and modern frontend practices. This adaptability allows me to contribute effectively to diverse projects and continue growing professionally."),
        ("Short test", "Short answer."),
    ]
    
    print("🧪 Injecting test content into message queue...")
    
    for i, (question, answer) in enumerate(test_cases):
        print(f"🧪 Injecting test case {i+1}: {question[:30]}...")
        message_queue.put((question, answer))
        time.sleep(2)  # Wait between injections
    
    print("🧪 All test content injected!")

if __name__ == "__main__":
    inject_test_content()