#!/bin/bash

# Activate virtual environment if you're using one (optional)
source /mnt/c/Users/Mahmoud/Desktop/EU/TERM_III/BusinessIntelligence/FinalProject/venv/bin/activate

# Navigate to the folder (replace with your actual path if needed)
cd "$(dirname "$0")"

echo "Running extract_weather.py"
python3 extract_weather.py

echo "Running clean_weather.py"
python3 clean_weather.py

echo "Running load_weather.py"
python3 load_weather.py

echo "ETL pipeline executed at $(date)"

deactivate