import sys
import os

# Add the directory to Python path to import core
sys.path.append('/Users/robertohernandez-macmini-m1/Desktop/Anthropic/Claude/INTERVIEW_TELEPROMPTER')

# Change working directory to ensure paths work correctly
os.chdir('/Users/robertohernandez-macmini-m1/Desktop/Anthropic/Claude/INTERVIEW_TELEPROMPTER')

from core import ask_gpt

# Test the REI-enhanced system
test_questions = [
    "Why do you want to work at REI?",
    "Tell me about your customer service philosophy",
    "How would you handle a difficult customer?",
    "What's your experience with outdoor gear?"
]

print("🧪 Testing REI-enhanced Interview Teleprompter system...\n")

for i, question in enumerate(test_questions, 1):
    print(f"Q{i}: {question}")
    try:
        answer = ask_gpt(question)
        print(f"A{i}: {answer}")
        print("-" * 80)
    except Exception as e:
        print(f"❌ Error: {e}")
        print("-" * 80)

print("✅ Test completed!")