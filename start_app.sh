#!/bin/bash

# Engineering Balloon Tool - Startup Script

echo ""
echo "========================================================================"
echo "             ENGINEERING BALLOON TOOL - STARTUP"
echo "========================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[SETUP] Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "[SETUP] Installing dependencies..."
    pip install flask pymupdf
else
    source venv/bin/activate
    # Ensure deps are there just in case
    if ! python3 -c "import fitz, flask" 2>/dev/null; then
         echo "[SETUP] Installing missing dependencies..."
         pip install flask pymupdf
    fi
fi

echo ""
echo "========================================================================"
echo "                    STARTING TOOL"
echo "========================================================================"
# Attempt to detect the primary IP address
IP_ADDR=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$IP_ADDR" ]; then
    IP_ADDR="localhost"
fi

echo "Server is running! Access it at:"
echo "  > http://$IP_ADDR:5001"
echo "Press Ctrl+C to stop the server"
echo ""

python3 engineering_balloon_tool.py
