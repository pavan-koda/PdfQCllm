#!/bin/bash
# Unified PDF QA System Startup Script
# Interactive model selection with vision-style indexing

set -e

echo "========================================================================"
echo "   UNIFIED PDF QA SYSTEM"
echo "   Interactive Model Selection + Vision-Style Indexing"
echo "========================================================================"
echo

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 not installed${NC}"
    echo "Install from https://www.python.org"
    exit 1
fi

echo "[1/5] Python 3 found ✓"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}ERROR: Ollama not installed${NC}"
    echo
    echo "Install Ollama:"
    echo "  macOS: brew install ollama"
    echo "  Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "  Or visit: https://ollama.ai/download"
    exit 1
fi

echo "[2/5] Ollama found ✓"
echo

# Create/activate virtual environment
if [ ! -d "venv" ]; then
    echo "[3/5] Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo "[3/5] Virtual environment exists ✓"
fi

source venv/bin/activate
echo

# Check/install dependencies
echo "[4/5] Checking dependencies..."

if ! python -c "import fitz" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install --upgrade pip --quiet
    pip install -r requirements_vision.txt --quiet
    echo -e "${GREEN}Dependencies installed${NC}"
else
    echo "Dependencies verified ✓"
fi
echo

# Start Ollama if not running
echo "[5/5] Checking Ollama server..."
if ! curl -s http://localhost:11434/api/tags &>/dev/null; then
    echo "Starting Ollama server..."

    if command -v systemctl &> /dev/null; then
        sudo systemctl start ollama || ollama serve &
    else
        ollama serve &
    fi

    sleep 3
    echo -e "${GREEN}Ollama server started${NC}"
else
    echo "Ollama server running ✓"
fi
echo

echo "========================================================================"
echo "   STARTING UNIFIED SYSTEM WITH COMPREHENSIVE MODEL SELECTOR"
echo "========================================================================"
echo
echo "You will be prompted to select from 53+ AI models..."
echo "Including: Ollama (Llama Vision, Gemma, Mistral, Phi, Qwen)"
echo "           HuggingFace (Gemma 1/2/3, GPT-2, FLAN-T5, Llama 2, etc.)"
echo

# Run the unified app (which will show comprehensive model selection menu)
python app_unified.py

# Cleanup
trap "echo 'Shutting down...'; deactivate; exit" INT TERM
