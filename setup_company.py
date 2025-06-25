#!/usr/bin/env python3
"""
Company Setup Automation for Interview Teleprompter
===================================================

This script automates the process of setting up the Interview Teleprompter
for a new company by:
1. Creating company-specific directory structure
2. Setting up ChromaDB collection for the company
3. Loading company knowledge chunks
4. Updating core.py with company-specific settings
5. Creating test files for verification

Usage:
    python3 setup_company.py --company "CompanyName" --role "Job Title"
    
Example:
    python3 setup_company.py --company "REI" --role "Store Sales Specialist"
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
import chromadb
from openai import OpenAI
import json
from datetime import datetime

class CompanySetup:
    def __init__(self, company_name, job_role):
        self.company_name = company_name
        self.job_role = job_role
        self.company_dir = Path(f"./{company_name}")
        self.chroma_collection_name = f"{company_name.lower()}_interview_chunks"
        self.knowledge_chunks_file = f"{company_name.lower()}_knowledge_chunks.txt"
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
        # Load OpenAI client
        from dotenv import load_dotenv
        load_dotenv()
        self.openai_client = OpenAI()
        
    def create_directory_structure(self):
        """Create company-specific directory structure"""
        print(f"📁 Creating directory structure for {self.company_name}...")
        
        self.company_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.company_dir / "backup").mkdir(exist_ok=True)
        
        print(f"✅ Directory structure created at {self.company_dir}")
        
    def create_knowledge_chunks_template(self):
        """Create a template knowledge chunks file"""
        knowledge_file = self.company_dir / self.knowledge_chunks_file
        
        if knowledge_file.exists():
            print(f"⚠️  Knowledge chunks file already exists: {knowledge_file}")
            return
            
        template_content = f"""# {self.company_name} Interview Knowledge Chunks
# 
# Add company-specific information here that will help generate
# relevant interview responses. Each section should be separated
# by blank lines for proper chunking.
#
# Example sections to include:
# - Company mission, values, and culture
# - Products and services
# - Recent news and developments
# - Job-specific requirements and responsibilities
# - Your relevant experience and skills
# - Why you want to work for this company

## Company Overview
{self.company_name} is a [add company description here]

## Company Values
[Add company values and culture information]

## Products/Services
[Add information about company products or services]

## Job Role: {self.job_role}
[Add specific information about the role you're applying for]

## Your Relevant Experience
[Add your relevant experience and skills that match this role]

## Why This Company
[Add reasons why you want to work for this company]

## Recent Company News
[Add any recent developments, news, or achievements]
"""
        
        knowledge_file.write_text(template_content)
        print(f"📝 Created knowledge chunks template: {knowledge_file}")
        print(f"🔍 Please edit {knowledge_file} with company-specific information before proceeding")
        
    def create_chunk_loader(self):
        """Create company-specific chunk loader script"""
        loader_file = f"load_{self.company_name.lower()}_chunks_to_chroma.py"
        
        loader_content = f'''#!/usr/bin/env python3
"""
Load {self.company_name} Knowledge Chunks to ChromaDB
"""

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

def load_chunks():
    """Load {self.company_name} knowledge chunks into ChromaDB"""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize clients
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    openai_client = OpenAI()
    
    # Create or get collection
    collection = chroma_client.get_or_create_collection(
        name="{self.chroma_collection_name}",
        metadata={{"company": "{self.company_name}", "role": "{self.job_role}"}}
    )
    
    # Read knowledge chunks
    chunks_file = "{self.company_name}/{self.knowledge_chunks_file}"
    
    if not os.path.exists(chunks_file):
        print(f"❌ Knowledge chunks file not found: {{chunks_file}}")
        print(f"Please create and populate {{chunks_file}} first")
        return False
        
    with open(chunks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into chunks (by double newlines)
    chunks = [chunk.strip() for chunk in content.split('\\n\\n') if chunk.strip()]
    
    print(f"📚 Found {{len(chunks)}} chunks to process")
    
    # Generate embeddings and store
    for i, chunk in enumerate(chunks):
        if len(chunk) < 20:  # Skip very short chunks
            continue
            
        # Generate embedding
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=chunk
        )
        embedding = response.data[0].embedding
        
        # Store in ChromaDB
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[f"{self.company_name.lower()}_chunk_{{i}}"]
        )
        
        print(f"✅ Processed chunk {{i+1}}/{{len(chunks)}}")
    
    print(f"🎉 Successfully loaded {{len(chunks)}} chunks for {self.company_name}")
    return True

if __name__ == "__main__":
    load_chunks()
'''
        
        with open(loader_file, 'w') as f:
            f.write(loader_content)
        
        # Make executable
        os.chmod(loader_file, 0o755)
        print(f"🔧 Created chunk loader: {loader_file}")
        
    def create_test_script(self):
        """Create company-specific test script"""
        test_file = f"test_{self.company_name.lower()}_system.py"
        
        test_content = f'''#!/usr/bin/env python3
"""
Test {self.company_name} Interview System
"""

from core import ask_gpt

def test_questions():
    """Test company-specific questions"""
    
    test_questions = [
        "Tell me about yourself and why you're interested in {self.company_name}",
        "What do you know about {self.company_name}?",
        "Why do you want to work as a {self.job_role}?",
        "What relevant experience do you have for this role?",
        "How would you contribute to {self.company_name}'s mission?"
    ]
    
    print(f"🧪 Testing {self.company_name} Interview System")
    print("="*50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\\n❓ Question {{i}}: {{question}}")
        print("-" * 40)
        
        try:
            response = ask_gpt(question)
            print(f"🤖 Response: {{response[:200]}}...")
            print("✅ Test passed")
        except Exception as e:
            print(f"❌ Test failed: {{e}}")
    
    print(f"\\n🎉 {self.company_name} system testing complete!")

if __name__ == "__main__":
    test_questions()
'''
        
        with open(test_file, 'w') as f:
            f.write(test_content)
            
        os.chmod(test_file, 0o755)
        print(f"🧪 Created test script: {test_file}")
        
    def update_core_py(self):
        """Update core.py with company-specific settings"""
        print(f"🔧 Updating core.py for {self.company_name}...")
        
        # Backup current core.py
        backup_file = f"{self.company_name}/backup/core_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        shutil.copy2("core.py", backup_file)
        print(f"💾 Backed up current core.py to {backup_file}")
        
        # Read current core.py
        with open("core.py", 'r') as f:
            content = f.read()
        
        # Update collection name and system prompt
        updated_content = content.replace(
            'collection = chroma_client.get_or_create_collection("interview_chunks")',
            f'collection = chroma_client.get_or_create_collection("{self.chroma_collection_name}")'
        )
        
        # Update system prompt if it exists
        if "system_prompt =" in updated_content:
            old_prompt_start = updated_content.find("system_prompt =")
            old_prompt_end = updated_content.find('"""', old_prompt_start + updated_content[old_prompt_start:].find('"""') + 3) + 3
            
            new_system_prompt = f'''system_prompt = """You are an AI assistant helping with interview responses for a {self.job_role} position at {self.company_name}.

Use the provided context to give specific, relevant, and personalized answers that:
1. Show deep knowledge of {self.company_name}
2. Demonstrate alignment with the {self.job_role} role
3. Highlight relevant experience and skills
4. Express genuine enthusiasm for the company and position

Keep responses concise, professional, and authentic. Use specific examples when possible.
"""'''
            
            updated_content = updated_content[:old_prompt_start] + new_system_prompt + updated_content[old_prompt_end:]
        
        # Write updated core.py
        with open("core.py", 'w') as f:
            f.write(updated_content)
            
        print(f"✅ Updated core.py for {self.company_name}")
        
    def create_setup_summary(self):
        """Create a setup summary file"""
        summary_file = f"{self.company_name}/{self.company_name.lower()}_setup_summary.md"
        
        summary_content = f"""# {self.company_name} Interview Setup Summary

**Company:** {self.company_name}  
**Role:** {self.job_role}  
**Setup Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**ChromaDB Collection:** {self.chroma_collection_name}

## Files Created

- `{self.company_name}/{self.knowledge_chunks_file}` - Knowledge base (EDIT THIS FIRST!)
- `load_{self.company_name.lower()}_chunks_to_chroma.py` - Chunk loader script
- `test_{self.company_name.lower()}_system.py` - Test script
- `{self.company_name}/backup/` - Backup directory

## Next Steps

1. **Edit Knowledge Base:**
   ```bash
   open {self.company_name}/{self.knowledge_chunks_file}
   ```
   Add company-specific information, values, recent news, etc.

2. **Load Chunks to ChromaDB:**
   ```bash
   python3 load_{self.company_name.lower()}_chunks_to_chroma.py
   ```

3. **Test the System:**
   ```bash
   python3 test_{self.company_name.lower()}_system.py
   ```

4. **Start Interview Teleprompter:**
   ```bash
   python3 interview_teleprompter.py
   ```

## Quick Warp Agent Setup

Copy and paste this prompt into Warp Agent:

```
Help me set up the Interview Teleprompter for {self.company_name}. I need you to:

1. Open {self.company_name}/{self.knowledge_chunks_file} and help me populate it with company information
2. Run load_{self.company_name.lower()}_chunks_to_chroma.py to load the knowledge base
3. Test the system with test_{self.company_name.lower()}_system.py
4. Start the interview teleprompter when ready

The system is set up for a {self.job_role} position at {self.company_name}.
```

## Reverting to Previous Company

To switch back to a previous company setup, restore the backup:

```bash
cp {self.company_name}/backup/core_backup_[timestamp].py core.py
```
"""
        
        with open(summary_file, 'w') as f:
            f.write(summary_content)
            
        print(f"📋 Created setup summary: {summary_file}")
        
    def run_setup(self):
        """Run the complete company setup process"""
        print(f"🚀 Setting up Interview Teleprompter for {self.company_name}")
        print(f"📋 Role: {self.job_role}")
        print("="*60)
        
        try:
            self.create_directory_structure()
            self.create_knowledge_chunks_template()
            self.create_chunk_loader()
            self.create_test_script()
            self.update_core_py()
            self.create_setup_summary()
            
            print("\n" + "="*60)
            print(f"🎉 Setup complete for {self.company_name}!")
            print(f"📋 Next steps:")
            print(f"   1. Edit {self.company_name}/{self.knowledge_chunks_file}")
            print(f"   2. Run: python3 load_{self.company_name.lower()}_chunks_to_chroma.py")
            print(f"   3. Test: python3 test_{self.company_name.lower()}_system.py")
            print(f"   4. Start: python3 interview_teleprompter.py")
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            return False
            
        return True

def main():
    parser = argparse.ArgumentParser(description="Set up Interview Teleprompter for a new company")
    parser.add_argument("--company", required=True, help="Company name (e.g., 'REI', 'Google')")
    parser.add_argument("--role", required=True, help="Job role (e.g., 'Store Sales Specialist')")
    
    args = parser.parse_args()
    
    setup = CompanySetup(args.company, args.role)
    setup.run_setup()

if __name__ == "__main__":
    main()
