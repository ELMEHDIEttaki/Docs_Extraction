#!/bin/bash

# Define the virtual environment directory
VENV_DIR="env"

# Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install langchain-community pypdf sentence-transformers chromadb requests sentencepiece torch

echo "Setup is complete. The virtual environment is activated."

# Run the main script
python src/main.py

