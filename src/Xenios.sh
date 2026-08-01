#!/bin/bash
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install it first."
    exit 1
fi

#check for tinker module
python3 -c "import tkinter" 2>/dev/null || {
    echo "tkinter not found. Install it with:"
    echo "  Ubuntu/Debian: sudo apt install python3-tk"
    echo "  Fedora:        sudo dnf install python3-tkinter"
    exit 1
}

python3 launcher.py
