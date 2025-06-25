# 🎤 Interview Teleprompter

**AI-powered real-time interview response assistant that generates contextual answers and displays them in a teleprompter-style window.**

⚡ *Simplified version using manual text input trigger instead of complex audio transcription software.*

---

## 📍 System Information

**Primary Development Location (Mac Mini):**
```
~/Desktop/Anthropic/Claude/INTERVIEW_TELEPROMPTER
```

**GitHub Repository:**
```
https://github.com/rohernan76/Interview-Teleprompter
```

---

## 🧠 How It Works

1. **Start the program:** Run `python3 interview_teleprompter.py`
2. **Input questions:** Open `whisper_output.txt` and type interview questions
3. **Save to trigger:** Save the file - this triggers the AI response generation
4. **View response:** AI-generated answer appears in the teleprompter window
5. **Repeat:** Continue adding new questions to get more responses

**Key Features:**
- Real-time file monitoring for question detection
- GPT-4 integration with contextual knowledge base
- Duplicate question detection and filtering
- Large-font teleprompter display with auto-sizing
- Comprehensive session logging

---

## 🚀 Quick Setup Guide

### 1. Prerequisites
- **Python 3.13+** (recommended)
- **OpenAI API Key** (required)
- **Git** (for syncing)

### 2. Initial Setup (Mac Mini - Primary Development)

```bash
# Navigate to the project directory
cd ~/Desktop/Anthropic/Claude/INTERVIEW_TELEPROMPTER

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Install dependencies
pip3 install -r requirements.txt

# Run the interview teleprompter
python3 interview_teleprompter.py
```

### 3. Setting Up Your OpenAI API Key

**IMPORTANT:** The `.env` file is excluded from the repository for security. You must create it manually:

```bash
# In the project root directory
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

Replace `your_actual_api_key_here` with your actual OpenAI API key from https://platform.openai.com/api-keys

---

## 💻 MacBook Pro Sync Instructions

### First Time Setup on MacBook Pro

```bash
# Clone the repository
cd ~/Desktop
git clone https://github.com/rohernan76/Interview-Teleprompter.git
cd Interview-Teleprompter

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Install dependencies
pip3 install -r requirements.txt

# Test the setup
python3 interview_teleprompter.py
```

### Syncing Updates from Main Branch

```bash
# Navigate to your local repository
cd ~/Desktop/Interview-Teleprompter  # or wherever you cloned it

# Fetch and pull latest changes
git fetch origin
git pull origin main

# Ensure .env file exists (create if missing)
# echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Update dependencies if needed
pip3 install -r requirements.txt

# Test the updated version
python3 interview_teleprompter.py
```

---

## 🎯 Usage Instructions

### Step-by-Step Operation

1. **Start the system:**
   ```bash
   cd ~/Desktop/Anthropic/Claude/INTERVIEW_TELEPROMPTER
   python3 interview_teleprompter.py
   ```

2. **You'll see output like:**
   ```
   📡 File monitor is now watching 'whisper_output.txt'...
   📱 Interview Teleprompter is running...
   ```

3. **Open the trigger file:**
   - Open `whisper_output.txt` in any text editor
   - Type your interview question (e.g., "Tell me about yourself")
   - **Save the file** (Cmd+S)

4. **Watch the magic:**
   - The system detects the new question
   - Generates an AI response using your knowledge base
   - Displays the answer in a teleprompter window

5. **Continue the interview:**
   - Add new questions to `whisper_output.txt`
   - Save after each question
   - Get instant AI-generated responses

### Tips for Best Results
- Type questions clearly and completely
- Save the file after each new question
- The system automatically filters duplicate questions
- All sessions are logged in the `Interview Logs/` folder

---

## 🤖 Warp Agent Setup Prompt

**Copy and paste this into Warp Agent for instant setup:**

```
Help me set up the Interview Teleprompter system. The project is located at ~/Desktop/Anthropic/Claude/INTERVIEW_TELEPROMPTER. I need you to:

1. Navigate to the project directory
2. Check if .env file exists, if not help me create it with my OpenAI API key
3. Install any missing Python dependencies from requirements.txt
4. Start the interview teleprompter program
5. Help me test it by adding a sample question to whisper_output.txt

The system works by monitoring whisper_output.txt for new questions, then generating AI responses displayed in a teleprompter window.
```

---

## 📂 Project Structure

```
INTERVIEW_TELEPROMPTER/
├── .env                           # OpenAI API key (create manually)
├── .gitignore                     # Git ignore rules
├── interview_teleprompter.py      # Main entry point
├── core.py                        # Core AI logic and file monitoring
├── gui.py                         # Teleprompter GUI components
├── whisper_output.txt             # Input file for questions
├── requirements.txt               # Python dependencies
├── knowledge_chunks.txt           # AI knowledge base
├── prep_notes.txt                 # Additional context notes
├── Interview Logs/                # Session logs directory
│   └── log_YYYY-MM-DD_HH-MM-SS.txt
├── chroma_db/                     # Vector database for AI context
├── backup_working/                # Development backups
├── REI/                          # REI-specific interview prep
└── MacWhisper Pro/               # Legacy transcription tools
```

---

## 🔧 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Ensure `.env` file exists in project root
- Check that your API key is valid and has credits

**"Permission denied" when running script**
- Run: `chmod +x interview_teleprompter.py`

**GUI window not appearing**
- Check console for error messages
- Ensure Python has accessibility permissions on macOS

**Questions not being detected**
- Make sure to **save** `whisper_output.txt` after adding questions
- Check that the file is in the same directory as the script

### Getting Help

For issues or questions:
1. Check the session logs in `Interview Logs/`
2. Review console output for error messages
3. Ensure all dependencies are installed
4. Verify your OpenAI API key is working

---

## 🎯 Recent Updates

- ✅ Simplified setup (removed MacWhisper/Loopback/Audio Hijack dependencies)
- ✅ Manual text input trigger system
- ✅ Enhanced security (`.env` file excluded from repository)
- ✅ Improved cross-device sync instructions
- ✅ Comprehensive documentation and setup guides
- ✅ Warp Agent integration prompt

---

## 📜 License

MIT License - see LICENSE file for details

---

## 🤝 Credits

Created by [@rohernan76](https://github.com/rohernan76)  
AI-powered by OpenAI GPT-4  
Developed with assistance from Claude (Anthropic)
