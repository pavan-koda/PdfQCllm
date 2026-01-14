# Files to Use - Unified PDF QA System

This document lists which files to use and which can be removed/ignored.

---

## ✅ FILES TO USE (Core System)

### Main Application Files
- **app_unified.py** - Main Flask application with unified model selector
- **unified_model_selector.py** - Comprehensive model selector (53+ models)
- **start_unified.sh** - Startup script for unified system

### PDF Processing & QA Engine
- **vision_pdf_processor.py** - PDF processing (text extraction, image rendering)
- **vision_qa_engine.py** - QA engine (ChromaDB, FAISS, ColPali integration)
- **colpali_retriever.py** - Visual document retrieval

### Templates (Web UI)
- **templates/vision_upload.html** - PDF upload page
- **templates/vision_qa.html** - Chat interface with timestamps, conversation history

### Configuration
- **requirements_vision.txt** - Python dependencies
- **UNIFIED_MODEL_SELECTOR_README.md** - Complete documentation

---

## ❌ FILES TO REMOVE/IGNORE (Obsolete/Redundant)

### Old Model Selectors (Replaced by unified_model_selector.py)
- ~~model_selector.py~~ - Old HuggingFace-only selector
- ~~model_selector_menu.py~~ - Old Ollama-only selector (21 models)

### Old Application Files (Replaced by app_unified.py)
- ~~app_vision.py~~ - Old vision-only app
- ~~app.py~~ - Original basic app
- ~~start_app.sh~~ - Old startup script

### Old Templates (If any duplicates exist)
- ~~templates/upload.html~~ - Old upload page (use vision_upload.html)
- ~~templates/qa.html~~ - Old chat page (use vision_qa.html)

### Development/Testing Files
- ~~test_*.py~~ - Any test files
- ~~debug_*.py~~ - Debug scripts
- ~~old_*.py~~ - Backup files

### Old Documentation (Replaced)
- ~~README.md~~ - Old readme (use UNIFIED_MODEL_SELECTOR_README.md)
- ~~UNIFIED_SYSTEM_README.md~~ - Old unified readme

---

## 📁 KEEP BUT DON'T MODIFY

### Deployment Folder (Separate system)
- **vision_qa_deployment/** - Complete deployment package for 12 systems
  - This is a standalone copy for deployment
  - Don't modify unless deploying to new systems

### Data/Cache Folders (Auto-generated)
- **uploads/** - Uploaded PDFs (auto-created)
- **processed_pdfs/** - Rendered page images (auto-created)
- **chroma_db/** - ChromaDB vector database (auto-created)
- **data/** - FAISS indexes (auto-created)
- **logs/** - Performance logs (auto-created)

---

## 🗂️ COMPLETE FILE STRUCTURE (Clean System)

```
PDF-QA-System/
├── app_unified.py                      ✅ Main Flask application
├── unified_model_selector.py           ✅ Model selector (53+ models)
├── start_unified.sh                    ✅ Startup script
├── vision_pdf_processor.py             ✅ PDF processing
├── vision_qa_engine.py                 ✅ QA engine
├── colpali_retriever.py                ✅ Visual retrieval
├── requirements_vision.txt             ✅ Dependencies
├── UNIFIED_MODEL_SELECTOR_README.md    ✅ Documentation
├── FILES_TO_USE.md                     ✅ This file
│
├── templates/
│   ├── vision_upload.html              ✅ Upload page
│   └── vision_qa.html                  ✅ Chat interface
│
├── vision_qa_deployment/               📦 Deployment package (separate)
│   └── ... (complete standalone system)
│
├── uploads/                            🔧 Auto-created
├── processed_pdfs/                     🔧 Auto-created
├── chroma_db/                          🔧 Auto-created
├── data/                               🔧 Auto-created
└── logs/                               🔧 Auto-created
```

---

## 🚀 HOW TO USE

### 1. Start the System
```bash
chmod +x start_unified.sh
./start_unified.sh
```

### 2. Select Your Model
You'll see a menu with 53+ models organized by category:
- Vision Models (2)
- Gemma Ollama (10)
- Gemma HuggingFace (13)
- Other Ollama (8)
- GPT-2 (4)
- Other HuggingFace (16)
- Custom (1)

### 3. System Starts
The system automatically:
- Downloads model if needed (Ollama)
- Initializes QA engine
- Starts web server at http://localhost:5000

### 4. Upload PDF & Ask Questions
Open browser to http://localhost:5000 and start using the system.

---

## 🔄 RE-SELECTING MODELS

To change models:
1. Stop server (Ctrl+C)
2. Run `./start_unified.sh` again
3. Select different model

The selector shows your selection history and lets you pick a new model each time.

---

## ✨ KEY FEATURES

### All Models in One Place
- **Ollama Models**: Llama Vision, Gemma 1/2, Mistral, Phi, Qwen
- **HuggingFace Models**: Gemma 1/2/3, GPT-2, OPT, FLAN-T5, Llama 2, TinyLlama, StableLM, Mistral, Phi, Qwen
- **Custom Models**: Enter any Ollama or HuggingFace model ID

### Automatic Management
- Auto-download for Ollama models
- Cache detection for HuggingFace models
- Installation status display
- Model recommendations highlighted

### All Previous Features Preserved
- ✅ Conversation history (last 5 Q&A)
- ✅ Message timestamps (client timezone)
- ✅ Complete answers (no truncation)
- ✅ Image display (diagrams, charts)
- ✅ Modal image viewer
- ✅ Smart vision detection
- ✅ Instant greeting responses
- ✅ Performance logging

---

## 📊 RECOMMENDED MODELS

### For Your Textbook Use Case
1. **Gemma 2 9B Instruct (Ollama)** - Option 11
2. **Gemma 3 4B Instruct (HuggingFace)** - Option 24
3. **Llama 3.2-Vision (11B)** - Option 1 (if diagrams)

### For Speed
- **Phi-3.5 Mini Instruct** - Option 31
- **FLAN-T5 Small** - Option 40

### For Vision
- **Llama 3.2-Vision (11B)** - Option 1 (only vision model)

---

## 🧹 CLEANUP COMMANDS

To remove old files:

```bash
# Remove old model selectors
rm model_selector.py model_selector_menu.py

# Remove old app files
rm app_vision.py app.py start_app.sh

# Remove old templates (if they exist)
rm templates/upload.html templates/qa.html 2>/dev/null || true

# Remove old documentation
rm UNIFIED_SYSTEM_README.md 2>/dev/null || true
```

After cleanup, your directory will only have the essential files listed above.

---

## 💡 NOTES

1. **Don't delete vision_qa_deployment/** - It's a complete standalone system for deploying to other machines

2. **Keep requirements_vision.txt** - Contains all Python dependencies

3. **Auto-created folders** (uploads/, processed_pdfs/, chroma_db/, data/, logs/) are created automatically when needed

4. **HuggingFace models** require additional setup:
   ```bash
   pip install transformers torch accelerate
   ```

5. **Ollama models** require Ollama to be installed and running:
   ```bash
   ollama serve
   ```

---

## ✅ SUMMARY

**Use these files:**
- app_unified.py
- unified_model_selector.py
- start_unified.sh
- vision_pdf_processor.py
- vision_qa_engine.py
- colpali_retriever.py
- requirements_vision.txt
- templates/vision_upload.html
- templates/vision_qa.html
- UNIFIED_MODEL_SELECTOR_README.md

**Remove these files:**
- model_selector.py
- model_selector_menu.py
- app_vision.py
- app.py
- start_app.sh
- Old templates and documentation

**Keep but don't modify:**
- vision_qa_deployment/ (deployment package)
- Auto-created folders (uploads/, processed_pdfs/, etc.)

---

## 🎯 READY TO USE!

```bash
./start_unified.sh
```

Select your model and start asking questions about your PDFs!
