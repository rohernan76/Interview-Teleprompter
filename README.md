# 🎤 Interview Teleprompter

**AI-powered desktop assistant that listens to interview questions, generates real-time responses using GPT-4, and displays them in a teleprompter-style overlay.**

---

## 📌 Overview

Interview Teleprompter is built for job seekers, speakers, and anyone practicing live Q&A. It combines live transcription (via MacWhisper or Whisper), GPT-generated answers, and a desktop GUI that scrolls the response in large-font for discreet prompting.

---

## ✨ Features

- ✅ Real-time transcription via `whisper_output.txt`
- ✅ Debounced, deduplicated question detection
- ✅ GPT-4 integration with prep notes context
- ✅ Big-font teleprompter overlay using Tkinter
- ✅ Logs all activity to timestamped text files
- ✅ AI-assisted development using Codex CLI

---

## 🧠 How It Works

1. Watch `whisper_output.txt` for new interviewer questions  
2. Debounce and dedupe inputs  
3. Send question + prep notes to GPT-4  
4. Display response in fullscreen scrolling GUI  
5. Log everything to `log_*.txt` and `codex_usage.md`

---

## 📂 Repo Structure

```
Interview-Teleprompter/
├── interview_teleprompter.py    # Main Python script
├── prep_notes.txt               # Your notes passed to GPT-4
├── whisper_output.txt           # Live transcription output
├── codex_usage.md               # Codex CLI prompt+response log
├── backup_working/              # Legacy versions
├── MacWhisper Pro/              # Optional transcription tool
└── log_*.txt                    # Timestamped session logs
```

---

## 🚀 Getting Started

> ⚠️ This project is under active development. For now, it’s tested locally on macOS via Python 3.13.

### Prerequisites
- Python 3.13+
- MacWhisper installed (or Whisper CLI alternative)
- OpenAI API key (set via env or `.zshrc`)
- Codex CLI (optional)

### Run the app
```bash
python3 interview_teleprompter.py
```

### Log Codex Prompts
```bash
~/Desktop/ResumeRocket/CodexTools/log_codex_interview.command "Prompt description here"
```

---

## 🎯 MVP Goals

- [x] Functional prototype on MacBook Pro
- [ ] Modularize code (GUI, core, config)
- [ ] Codex-enhanced refactors + docs
- [ ] GitHub Pages demo + walkthrough
- [ ] Test on iMac + mini for full setup sync

---

## 📜 License

[To Be Added] – MIT or Apache 2.0 likely

---

## 🤝 Credits

Created by [@rohernan76](https://github.com/rohernan76)  
AI-assisted by Codex CLI (OpenAI)  
Transcription powered by [MacWhisper](https://goodtech.ai/macwhisper)