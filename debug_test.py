#!/usr/bin/env python3
"""Debug script to test the core functionality."""

import os
from dotenv import load_dotenv
from core import ask_gpt, message_queue

# Load environment variables
load_dotenv()

def test_response_generation():
    """Test if we can generate a response."""
    try:
        print("🧪 Testing response generation...")
        question = "Why do you want to work for REI?"
        print(f"📝 Question: {question}")
        
        answer = ask_gpt(question)
        print(f"✅ Answer generated: {answer[:100]}...")
        
        # Test if message queue works
        message_queue.put((question, answer))
        print(f"📮 Message added to queue. Queue size: {message_queue.qsize()}")
        
        if not message_queue.empty():
            q, a = message_queue.get()
            print(f"📬 Retrieved from queue - Q: {q[:50]}...")
            print(f"📬 Retrieved from queue - A: {a[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_response_generation()
