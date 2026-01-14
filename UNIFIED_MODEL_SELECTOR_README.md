# Unified PDF QA System - Comprehensive Model Selector

Complete model selection system supporting **53+ AI models** across Ollama and HuggingFace platforms.

---

## Quick Start

```bash
chmod +x start_unified.sh
./start_unified.sh
```

You'll see a comprehensive menu with all available models organized by category.

---

## Available Models (53+ Options)

### Vision Models (2 options)
**Can read scanned PDFs, diagrams, charts**

1. **Llama 3.2-Vision (11B)** [RECOMMENDED]
   - Size: 7 GB (Ollama)
   - Speed: Medium
   - Best for: Scanned PDFs, diagrams, technical documents
   - Vision Support: Yes

2. **Llama 3.2-Vision (90B)**
   - Size: 55 GB (Ollama)
   - Speed: Slow
   - Best for: Ultimate quality (requires 64GB+ RAM)
   - Vision Support: Yes

---

### Gemma Models - Ollama (10 options)
**Fast setup, easy use, optimized for Ollama**

3. Gemma 2B (Ollama) - 1.5 GB, Fast
4. Gemma 7B (Ollama) - 5 GB, Medium
5. Gemma 2B Instruct (Ollama) - 1.5 GB, Fast
6. Gemma 7B Instruct (Ollama) - 5 GB, Medium
7. Gemma 2 2B (Ollama) - 1.6 GB, Fast
8. **Gemma 2 9B (Ollama)** [RECOMMENDED] - 5.5 GB, Medium
9. Gemma 2 27B (Ollama) - 16 GB, Slow
10. Gemma 2 2B Instruct (Ollama) - 1.6 GB, Fast
11. **Gemma 2 9B Instruct (Ollama)** [RECOMMENDED] - 5.5 GB, Medium
12. Gemma 2 27B Instruct (Ollama) - 16 GB, Slow

---

### Gemma Models - HuggingFace (13 options)
**More variants, GPU optimized, includes Gemma 3**

13. Gemma 2B (HF) - google/gemma-2b - 5 GB, Fast
14. Gemma 7B (HF) - google/gemma-7b - 14 GB, Slow
15. Gemma 2B Instruct (HF) - google/gemma-2b-it - 5 GB, Fast
16. Gemma 7B Instruct (HF) - google/gemma-7b-it - 14 GB, Slow
17. Gemma 2 2B (HF) - google/gemma-2-2b - 5 GB, Fast
18. Gemma 2 9B (HF) - google/gemma-2-9b - 18 GB, Slow
19. Gemma 2 2B Instruct (HF) - google/gemma-2-2b-it - 5 GB, Fast
20. **Gemma 2 9B Instruct (HF)** [RECOMMENDED] - google/gemma-2-9b-it - 18 GB, Slow
21. Gemma 2 27B Instruct (HF) - google/gemma-2-27b-it - 54 GB, Very Slow
22. Gemma 3 4B (HF) - google/gemma-3-4b - 8 GB, Fast
23. Gemma 3 12B (HF) - google/gemma-3-12b - 24 GB, Medium
24. **Gemma 3 4B Instruct (HF)** [RECOMMENDED] - google/gemma-3-4b-it - 8 GB, Fast
25. Gemma 3 12B Instruct (HF) - google/gemma-3-12b-it - 24 GB, Medium

---

### Other Ollama Models (8 options)
**Llama, Mistral, Phi, Qwen**

26. Llama 3.2 Text (3B) - 2 GB, Fast
27. Mistral 7B - 4 GB, Fast
28. Mistral 7B Instruct - 4 GB, Fast
29. Phi-3 Mini (3.8B) - 2.3 GB, Fast
30. Phi-3 Mini 4K Instruct - 2.3 GB, Fast
31. Phi-3.5 Mini Instruct - 2.3 GB, Fast
32. Qwen 2.5 7B Instruct - 4.7 GB, Medium
33. Qwen 2.5 14B Instruct - 9 GB, Medium

---

### GPT-2 Models (4 options)
**HuggingFace text generation models**

34. GPT-2 Small - gpt2 - 500 MB, Fast
35. GPT-2 Medium - gpt2-medium - 1.5 GB, Medium
36. GPT-2 Large - gpt2-large - 3 GB, Slower
37. GPT-2 XL - gpt2-xl - 6 GB, Very Slow

---

### Other HuggingFace Models (16 options)
**OPT, FLAN-T5, Phi, TinyLlama, StableLM, Llama 2, Mistral, Qwen**

38. OPT-350M - facebook/opt-350m - 700 MB, Fast
39. OPT-1.3B - facebook/opt-1.3b - 2.5 GB, Medium
40. FLAN-T5 Small - google/flan-t5-small - 300 MB, Fast
41. FLAN-T5 Base - google/flan-t5-base - 900 MB, Medium
42. FLAN-T5 Large - google/flan-t5-large - 3 GB, Slower
43. Phi-2 - microsoft/phi-2 - 5.5 GB, Medium
44. TinyLlama Chat - TinyLlama/TinyLlama-1.1B-Chat-v1.0 - 2.2 GB, Fast
45. StableLM Zephyr 1.6B - stabilityai/stablelm-2-zephyr-1_6b - 3 GB, Medium
46. Llama 2 7B Chat - meta-llama/Llama-2-7b-chat-hf - 13 GB, Slow
47. Llama 2 13B Chat - meta-llama/Llama-2-13b-chat-hf - 26 GB, Very Slow
48. Mistral 7B Instruct (HF) - mistralai/Mistral-7B-Instruct-v0.3 - 14 GB, Medium
49. Mistral 12B Instruct (HF) - mistralai/Mistral-12B-Instruct-v0.3 - 24 GB, Slower
50. Phi-3 Mini 4K (HF) - microsoft/Phi-3-mini-4k-instruct - 7.5 GB, Fast
51. Phi-3.5 Mini (HF) - microsoft/Phi-3.5-mini-instruct - 7.5 GB, Fast
52. Qwen 2.5 7B Instruct (HF) - Qwen/Qwen2.5-7B-Instruct - 14 GB, Medium
53. Qwen 2.5 14B Instruct (HF) - Qwen/Qwen2.5-14B-Instruct - 28 GB, Slower

---

### Custom Model (1 option)

99. **Custom Model** - Enter your own Ollama or HuggingFace model

---

## How It Works

```
Start unified system
    ↓
Display comprehensive menu (53+ models)
    ↓
User selects model by number
    ↓
System checks if model is installed
    ↓
Auto-download if needed (Ollama) or download on first use (HF)
    ↓
Initialize QA engine with selected model
    ↓
Configure vision support based on model
    ↓
Start Flask web server
    ↓
Ready for PDF upload and Q&A!
```

---

## Model Selection Guide

### For Textbooks (Your Use Case)

**Best Choice**: Gemma 2 9B Instruct (Ollama or HF)
- Excellent for technical/educational content
- Fast enough for interactive use
- Detailed, accurate answers
- No vision needed for text PDFs

**Alternative**: Gemma 3 4B Instruct (HF)
- Latest generation Gemma
- Best-in-class for QA tasks
- Lighter than 9B variant
- Very fast responses

### For Scanned Documents

**Best Choice**: Llama 3.2-Vision (11B)
- Only vision model available
- Can read text from images
- Handles diagrams and charts
- Essential for scanned PDFs

### For Speed

**Best Choice**:
- Phi-3.5 Mini Instruct (Ollama) - Fastest, good quality
- FLAN-T5 Small (HF) - Very fast, instruction-tuned
- GPT-2 Small (HF) - Ultra-fast, basic quality

### For Accuracy

**Best Choice**:
- Gemma 2 9B Instruct (Ollama/HF) - Best balance
- Gemma 3 12B Instruct (HF) - Premium quality
- Llama 3.2-Vision (11B) - For visual content

### For Multilingual Support

**Best Choice**:
- Qwen 2.5 7B/14B Instruct - Strong multilingual
- Gemma models - Good multilingual support

---

## Platform Comparison

### Ollama Models
✅ Easy setup (one command: `ollama pull model`)
✅ Auto-managed (downloads, caching, serving)
✅ Optimized for CPU/GPU
✅ Lower memory usage
✅ Works out of the box
❌ Fewer model variants
❌ Limited to Ollama-supported models

### HuggingFace Models
✅ Huge model selection (thousands)
✅ Latest models (Gemma 3, GPT-OSS, etc.)
✅ Direct from source
✅ Full control over configuration
❌ Requires more setup
❌ Manual GPU/VRAM management
❌ Downloads on first use (can be slow)
❌ Needs transformers, torch, accelerate

---

## Installation & Requirements

### For Ollama Models
```bash
# Install Ollama
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
# Windows: Download from https://ollama.ai/download

# Models download automatically when selected
```

### For HuggingFace Models
```bash
# Install Python dependencies
pip install transformers torch accelerate

# Models download automatically on first use
# Will be cached in ~/.cache/huggingface/
```

---

## Switching Models

To use a different model:

1. Stop the current server (Ctrl+C)
2. Run `./start_unified.sh` again
3. Select a different model from the menu

The system automatically reconfigures for the selected model.

---

## Technical Features

### All Vision System Features Included
✅ Conversation history (last 5 exchanges)
✅ Message timestamps (client timezone)
✅ Improved accuracy (complete answers)
✅ Image loading (diagrams, charts)
✅ Modal image viewer
✅ Stricter vision detection
✅ Smart context injection
✅ Instant greeting responses

### Plus New Features
✅ **53+ model options**
✅ **Both Ollama and HuggingFace support**
✅ **All Gemma generations (1, 2, 3)**
✅ **Interactive command-line selection**
✅ **Automatic model download**
✅ **Model status display**
✅ **Custom model support**
✅ **Re-selection on restart**

---

## File Structure

```
PDF-QA-System/
├── app_unified.py                    # Main app with model selection
├── unified_model_selector.py         # Comprehensive model selector
├── start_unified.sh                  # Startup script
├── vision_qa_engine.py               # QA engine
├── vision_pdf_processor.py           # PDF processing
├── colpali_retriever.py              # Visual search
├── templates/
│   ├── vision_upload.html
│   └── vision_qa.html
└── UNIFIED_MODEL_SELECTOR_README.md  # This file
```

---

## Configuration

### Use Specific Model Without Menu

Edit `app_unified.py` before the model selection:

```python
# Skip interactive menu, use specific model
model_selection = ('ollama', 'gemma2:9b-instruct', False)
# model_selection = select_model_interactive()  # Comment out
```

### Change Default Port

Edit `app_unified.py` line 372:

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

## Troubleshooting

### Model Not Downloading (Ollama)
```bash
# Manually download
ollama pull gemma2:9b-instruct

# Check available models
ollama list
```

### HuggingFace Model Not Loading
```bash
# Install required packages
pip install transformers torch accelerate

# For Llama 2 models, login to HuggingFace
huggingface-cli login
```

### Out of Memory (HuggingFace)
```bash
# Use smaller model
# Or enable CPU offload in vision_qa_engine.py

# For GPU: Check VRAM
nvidia-smi

# Use models within your VRAM limit
# 8GB VRAM: Use models up to ~7B params
# 16GB VRAM: Use models up to ~13B params
# 24GB VRAM: Use models up to ~27B params
```

### Port Already in Use
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill process
kill -9 <PID>

# Or change port in app_unified.py
```

---

## Performance Comparison

| Model | Platform | Size | Speed | Accuracy | Best For |
|-------|----------|------|-------|----------|----------|
| Llama 3.2-Vision 11B | Ollama | 7GB | Medium | Excellent | Scanned PDFs |
| Gemma 2 9B Instruct | Ollama | 5.5GB | Medium | Excellent | Technical QA |
| Gemma 3 4B Instruct | HuggingFace | 8GB | Fast | Exceptional | Best QA quality |
| Mistral 7B Instruct | Ollama | 4GB | Fast | Very Good | General purpose |
| Phi-3.5 Mini | Ollama | 2.3GB | Fast | Excellent | Quick responses |
| FLAN-T5 Large | HuggingFace | 3GB | Slower | Excellent | Instruction following |
| GPT-2 Small | HuggingFace | 500MB | Very Fast | Basic | Simple tasks |

---

## Example Usage

### Selecting Gemma 2 9B Instruct (Ollama)

```
Select model (1-53, 99 for custom) or 0 to exit: 11

================================================================================
Selected: Gemma 2 9B Instruct (Ollama)
Model ID: gemma2:9b-instruct
Type: ollama
Vision Support: No
Description: Gemma 2 instruction-tuned 9B, best quality
================================================================================

Proceed with this model? (y/n): y

Model not installed. Downloading gemma2:9b-instruct...
This may take several minutes.

Download now? (y/n): y

Downloading gemma2:9b-instruct...
SUCCESS: gemma2:9b-instruct downloaded!

================================================================================
  SYSTEM READY
================================================================================
Model: gemma2:9b-instruct
Model Type: Ollama
Ollama URL: http://localhost:11434
Vision Support: Disabled
ColPali Enabled: True
================================================================================

Starting server at: http://localhost:5000
Press Ctrl+C to stop
```

### Selecting Gemma 3 4B Instruct (HuggingFace)

```
Select model (1-53, 99 for custom) or 0 to exit: 24

================================================================================
Selected: Gemma 3 4B Instruct (HuggingFace)
Model ID: google/gemma-3-4b-it
Type: huggingface
Vision Support: No
Description: Gemma 3 instruction-tuned 4B, best-in-class QA
================================================================================

Proceed with this model? (y/n): y

NOTE: HuggingFace model will be downloaded on first use
Make sure you have sufficient disk space and GPU memory

NOTE: HuggingFace model support is experimental
The system will attempt to use the model, but functionality may be limited

================================================================================
  SYSTEM READY (EXPERIMENTAL HF MODE)
================================================================================
Model: google/gemma-3-4b-it
Model Type: HuggingFace
Vision Support: Disabled
ColPali Enabled: True

WARNING: HuggingFace models require additional setup
Please ensure you have transformers, torch, and accelerate installed
================================================================================

Starting server at: http://localhost:5000
Press Ctrl+C to stop
```

---

## Recommended Models

### Top 5 for Your Textbook Use Case

1. **Gemma 2 9B Instruct (Ollama)** - Best balance of speed and accuracy
2. **Gemma 3 4B Instruct (HuggingFace)** - Latest Gemma, excellent QA
3. **Llama 3.2-Vision (11B)** - If textbook has diagrams
4. **Mistral 7B Instruct (Ollama)** - Fast and accurate alternative
5. **Phi-3.5 Mini Instruct (Ollama)** - Best for quick responses

---

## Summary

- **53+ AI models** available
- **All Gemma generations** (1, 2, 3) included
- **Both Ollama and HuggingFace** platforms
- **Vision support** for scanned PDFs
- **Easy model switching** - just restart and select
- **All existing features** preserved (conversation history, timestamps, etc.)

Start exploring with:
```bash
./start_unified.sh
```

Select the model that best fits your needs!
