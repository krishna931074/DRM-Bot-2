#!/bin/bash
echo "Starting the bot..."
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 main.py
