# Unified PDF QA System - Interactive Model Selection

Combines the best of both worlds:
- ✅ Vision-style indexing (ChromaDB + FAISS + ColPali)
- ✅ Interactive model selection from command line
- ✅ All improvements (conversation history, timestamps, etc.)
- ✅ Support for multiple AI models

---

## 🚀 Quick Start

### Run the Unified System

```bash
chmod +x start_unified.sh
./start_unified.sh
```

You'll see an interactive menu:

```
================================================================================
  PDF QA SYSTEM - MODEL SELECTOR
================================================================================

✓ Ollama installed | 3 model(s) available

Available Models:
--------------------------------------------------------------------------------

1. Llama 3.2-Vision (11B) [RECOMMENDED] 👁️
   Type: OLLAMA
   Description: Best for vision + text, handles scanned PDFs
   Size: 7 GB | Status: ✓ Installed

2. Llama 3.2 Text (3B)
   Type: OLLAMA
   Description: Faster text-only model, good accuracy
   Size: 2 GB | Status: ⬇ Download

3. Gemma 2 (9B)
   Type: OLLAMA
   Description: Google model, excellent for technical content
   Size: 5.5 GB | Status: ⬇ Download

4. Mistral (7B)
   Type: OLLAMA
   Description: Fast and accurate, good for general use
   Size: 4 GB | Status: ⬇ Download

5. Phi-3 Mini (3.8B)
   Type: OLLAMA
   Description: Smallest model, fastest responses
   Size: 2.3 GB | Status: ⬇ Download

6. Custom Ollama Model
   Type: OLLAMA
   Description: Enter your own Ollama model name
   Size: Varies | Status: ⬇ Download

================================================================================

0. Exit

Select model (1-6) or 0 to exit:
```

Just type the number and press Enter!

---

## 📋 Available Models

### 1. Llama 3.2-Vision (11B) - [RECOMMENDED]
- **Best for**: Scanned PDFs, diagrams, technical documents
- **Vision Support**: Yes 👁️
- **Speed**: Medium (60-150s for vision, 10-20s for text)
- **Accuracy**: Excellent
- **Use when**: Need to read images, charts, or scanned documents

### 2. Llama 3.2 Text (3B)
- **Best for**: Text-only PDFs, faster responses
- **Vision Support**: No
- **Speed**: Fast (5-15s)
- **Accuracy**: Good
- **Use when**: PDF has proper text extraction

### 3. Gemma 2 (9B)
- **Best for**: Technical content, detailed answers
- **Vision Support**: No
- **Speed**: Medium (15-25s)
- **Accuracy**: Excellent for technical topics
- **Use when**: Need deep technical understanding

### 4. Mistral (7B)
- **Best for**: General purpose, balanced performance
- **Vision Support**: No
- **Speed**: Fast (10-20s)
- **Accuracy**: Very good
- **Use when**: General Q&A on text PDFs

### 5. Phi-3 Mini (3.8B)
- **Best for**: Quick answers, simple questions
- **Vision Support**: No
- **Speed**: Very fast (5-10s)
- **Accuracy**: Good
- **Use when**: Need speed over deep analysis

### 6. Custom Model
- **Best for**: Testing your own Ollama models
- **Configure**: Enter any Ollama model name
- **Example**: `gemma3:27b`, `llama3.1:8b`, etc.

---

## 🎯 Features

### All the Improvements from Vision System
✅ Conversation history (last 5 exchanges)
✅ Message timestamps (client timezone)
✅ Improved accuracy (complete answers)
✅ Image loading (diagrams, charts)
✅ Modal image viewer
✅ Stricter vision detection
✅ Smart context injection
✅ Instant greeting responses

### Plus New Features
✅ **Interactive model selection** at startup
✅ **Automatic model download** if not installed
✅ **Model status display** (installed vs download)
✅ **Flexible model support** (any Ollama model)
✅ **Vision detection** based on selected model
✅ **Custom model support**

---

## 🔄 Switching Models

To use a different model:

1. Stop the current server (Ctrl+C)
2. Run `./start_unified.sh` again
3. Select a different model from the menu

The system will automatically configure for the selected model.

---

## 💡 Model Selection Guide

### For Textbooks (Your Use Case)

**Best Choice**: Gemma 2 (9B)
- Excellent for technical/educational content
- Fast enough for interactive use
- Detailed, accurate answers
- No vision needed for text PDFs

**Alternative**: Llama 3.2-Vision (11B)
- Use if textbook has many diagrams
- Can read scanned/image pages
- Slower but more versatile

### For Scanned Documents

**Best Choice**: Llama 3.2-Vision (11B)
- Only model with vision support
- Can read text from images
- Handles diagrams and charts

### For Speed

**Best Choice**: Phi-3 Mini (3.8B)
- Fastest responses
- Good enough for simple Q&A
- Low resource usage

### For Accuracy

**Best Choice**: Gemma 2 (9B) or Llama 3.2-Vision (11B)
- Most detailed answers
- Best understanding of complex topics
- Worth the extra time

---

## 🛠️ Technical Details

### How It Works

```
Start unified system
    ↓
Show model selection menu
    ↓
User selects model (e.g., Gemma 2)
    ↓
Check if model is installed
    ↓
Download if needed (automatic)
    ↓
Initialize QA engine with selected model
    ↓
Configure vision support based on model
    ↓
Start Flask web server
    ↓
Ready for PDF upload and Q&A!
```

### Indexing System (Same as Vision)

**Step 1**: PDF Processing
- Extract text from each page
- Render each page as image (150 DPI)
- Extract embedded images

**Step 2**: Create Indexes
- **ChromaDB**: Text semantic search
- **FAISS**: Fast vector similarity
- **ColPali**: Visual similarity (if vision enabled)

**Step 3**: Smart Retrieval
- Search all indexes
- Pick best pages
- Extract relevant context
- Generate answer with selected model

---

## 📁 File Structure

```
PDF-QA-System/
├── app_unified.py              # Main unified app
├── model_selector_menu.py      # Interactive model selector
├── start_unified.sh            # Startup script
├── vision_qa_engine.py         # QA engine (works with any model)
├── vision_pdf_processor.py     # PDF processing
├── colpali_retriever.py        # Visual search
└── templates/
    ├── vision_upload.html      # Upload page
    └── vision_qa.html          # Chat interface
```

---

## 🔧 Configuration

### Change Default Model

Edit `start_unified.sh` to skip menu and use specific model:

```bash
# Add this before "python app_unified.py"
export DEFAULT_MODEL="gemma2:9b"
export SKIP_MENU="true"
```

### Change Port

Edit `app_unified.py` line 465:

```python
app.run(host='0.0.0.0', port=5001, debug=False)  # Changed from 5000
```

### Adjust Model Parameters

Edit `vision_qa_engine.py` lines 536-539:

```python
"num_predict": 2048,      # Max answer length
"temperature": 0.3,       # Lower = more factual
"num_ctx": 4096,         # Context window
"num_thread": 8          # CPU threads
```

---

## 🐛 Troubleshooting

### Model Not Downloading
```bash
# Manually download
ollama pull gemma2:9b

# Check available models
ollama list
```

### Port Already in Use
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill process
kill -9 <PID>

# Or change port in app_unified.py
```

### Ollama Not Running
```bash
# Start Ollama
ollama serve

# Or use systemd
sudo systemctl start ollama
```

### Vision Not Working
- Only Llama 3.2-Vision supports vision
- Other models are text-only
- System will auto-detect based on model selection

---

## 📊 Performance Comparison

| Model | Speed | Accuracy | Vision | Best For |
|-------|-------|----------|--------|----------|
| Llama 3.2-Vision | Medium-Slow | Excellent | Yes | Scanned PDFs, diagrams |
| Gemma 2 | Medium | Excellent | No | Technical content |
| Mistral | Fast | Very Good | No | General Q&A |
| Llama 3.2 Text | Fast | Good | No | Simple questions |
| Phi-3 Mini | Very Fast | Good | No | Quick lookups |

---

## 🎓 Example: Your Nuts Question

With **Gemma 2 (9B)** selected:

```
Question: types of nuts for special purpose

Answer (Complete, 12s response):
There are six types of nuts for special purposes:

1. Flanged nut (fig. 24-7): This is a hexagonal nut with a washer...
   [Full description with all technical details]

2. Cap nut (fig. 24-8): It is also a hexagonal nut provided with...
   [Complete specification]

3. Dome nut (fig. 24-9): It is a form of a cap nut having...
   [All details included]

4. Cylindrical or capstan nut (fig. 24-10): This nut is cylindrical...
   [Complete description]

5. Ring nut (fig. 24-11): It is in the form of a ring provided...
   [Full specification]

6. Wing nut (fig. 24-12): This nut can be easily operated...
   [Complete details]

🕐 14:30:45 | ⏱️ 12.3s | ⚡ Text-only mode | 📄 Page 601
```

**Result**: All 6 nuts, complete details, fast response!

---

## 🚀 Ready to Use!

```bash
./start_unified.sh
```

Select your model and start asking questions about your PDFs!

---

**Recommendation for your textbooks**: Use **Gemma 2 (9B)** for best accuracy on technical content.
