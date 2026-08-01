#!/bin/bash
cd "$(dirname "$0")"

# ── Python check ────────────────────────────────────────────────────────
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install it first."
    exit 1
fi

# ── Tkinter check ───────────────────────────────────────────────────────
python3 -c "import tkinter" 2>/dev/null || {
    echo "tkinter not found. Installing..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm tk
    elif command -v apt &> /dev/null; then
        sudo apt install -y python3-tk
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-tkinter
    else
        echo "Could not install tkinter automatically. Please install it manually."
        exit 1
    fi
}

# ── Pip check ───────────────────────────────────────────────────────────
if command -v pip3 &> /dev/null; then
    PIP="pip3"
elif command -v pip &> /dev/null; then
    PIP="pip"
elif python3 -m pip --version &> /dev/null; then
    PIP="python3 -m pip"
else
    echo "pip not found. Installing..."
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python-pip
    elif command -v apt &> /dev/null; then
        sudo apt install -y python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    else
        echo "Could not install pip automatically. Please install it manually."
        exit 1
    fi
    PIP="python3 -m pip"
fi

# ── Dependencies ────────────────────────────────────────────────────────
echo "Checking dependencies..."
$PIP install --quiet pillow

# ── Launch ──────────────────────────────────────────────────────────────
echo "Starting Xenios..."
python3 Xenios_EN.py
