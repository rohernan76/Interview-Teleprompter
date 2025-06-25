# 🏢 Company Setup Quick Reference Guide

## 🚀 One-Command Company Setup

Setting up the Interview Teleprompter for a new company is now automated! Simply run:

```bash
python3 setup_company.py --company "CompanyName" --role "Job Title"
```

### Examples:
```bash
# REI Setup
python3 setup_company.py --company "REI" --role "Store Sales Specialist"

# Google Setup  
python3 setup_company.py --company "Google" --role "Software Engineer"

# Tesla Setup
python3 setup_company.py --company "Tesla" --role "Manufacturing Engineer"
```

---

## 📋 What Gets Created Automatically

The setup script creates everything you need:

### 📁 Directory Structure
```
CompanyName/
├── companyname_knowledge_chunks.txt    # Knowledge base template
├── backup/                             # Core.py backups
└── companyname_setup_summary.md        # Setup instructions
```

### 🔧 Generated Scripts
- `load_companyname_chunks_to_chroma.py` - Loads knowledge to ChromaDB
- `test_companyname_system.py` - Tests company-specific responses
- Updated `core.py` with company-specific settings

---

## 🔄 4-Step Workflow After Setup

### 1. Edit Knowledge Base 📝
```bash
open CompanyName/companyname_knowledge_chunks.txt
```
Fill in company-specific information (mission, values, recent news, etc.)

### 2. Load Knowledge to ChromaDB 📚
```bash
python3 load_companyname_chunks_to_chroma.py
```

### 3. Test the System 🧪
```bash
python3 test_companyname_system.py
```

### 4. Start Interview Teleprompter 🎤
```bash
python3 interview_teleprompter.py
```

---

## 🤖 Warp Agent Integration

Each company setup generates a custom Warp Agent prompt. Just copy and paste from the setup summary file!

**Example for REI:**
```
Help me set up the Interview Teleprompter for REI. I need you to:

1. Open REI/rei_knowledge_chunks.txt and help me populate it with company information
2. Run load_rei_chunks_to_chroma.py to load the knowledge base
3. Test the system with test_rei_system.py  
4. Start the interview teleprompter when ready

The system is set up for a Store Sales Specialist position at REI.
```

---

## 🔄 Switching Between Companies

### Current Company Tracking
The system automatically backs up your `core.py` when switching companies.

### Reverting to Previous Company
```bash
# List available backups
ls CompanyName/backup/

# Restore a specific backup
cp CompanyName/backup/core_backup_20250625_123456.py core.py

# Load the previous company's chunks
python3 load_companyname_chunks_to_chroma.py
```

---

## 📊 Real-World Example: REI to Google

```bash
# Currently set up for REI, want to apply to Google

# 1. Set up Google 
python3 setup_company.py --company "Google" --role "Software Engineer"

# 2. Edit Google knowledge base
open Google/google_knowledge_chunks.txt
# Add Google-specific info...

# 3. Load Google chunks
python3 load_google_chunks_to_chroma.py

# 4. Test Google system
python3 test_google_system.py

# 5. Start teleprompter (now optimized for Google)
python3 interview_teleprompter.py

# Later: Switch back to REI
cp REI/backup/core_backup_20250625_120000.py core.py
python3 load_rei_chunks_to_chroma.py
python3 interview_teleprompter.py
```

---

## 🎯 Knowledge Base Best Practices

### Essential Sections to Include:
- **Company Overview** - Mission, values, culture
- **Products/Services** - What they do, recent launches
- **Recent News** - Latest developments, achievements
- **Role-Specific Info** - Job requirements, expectations
- **Your Fit** - Relevant experience, skills, examples
- **Why This Company** - Genuine reasons for interest

### Tips:
- Use specific facts and numbers when possible
- Include recent company news (last 6 months)
- Add industry context and competitors
- Mention specific technologies or methodologies they use
- Include your relevant projects and achievements

---

## 🔧 Troubleshooting

### "ChromaDB collection already exists"
This is normal - the system will use the existing collection.

### "Knowledge chunks file not found"
Make sure you've edited and saved the knowledge chunks file before loading.

### "OpenAI API error"
Check your `.env` file has a valid OpenAI API key.

### Core.py backup issues
Check the `CompanyName/backup/` directory for available backups.

---

## 📈 Advanced Usage

### Custom Knowledge Base Format
The system splits knowledge by double newlines (`\n\n`). Structure your knowledge base with clear sections separated by blank lines.

### Multiple Roles at Same Company
```bash
python3 setup_company.py --company "Google" --role "Product Manager"
python3 setup_company.py --company "Google" --role "Data Scientist"
```

### Batch Company Setup
Create a setup script for multiple companies:
```bash
#!/bin/bash
python3 setup_company.py --company "Google" --role "Software Engineer"
python3 setup_company.py --company "Apple" --role "iOS Developer"  
python3 setup_company.py --company "Microsoft" --role "Cloud Engineer"
```

---

## 🎉 Success Stories

**Before:** Manual 16-step process taking 30+ minutes per company
**After:** 4-step automated process taking 5-10 minutes per company

The automation handles all the technical ChromaDB setup, file generation, and core.py modifications that previously required manual coding changes.
