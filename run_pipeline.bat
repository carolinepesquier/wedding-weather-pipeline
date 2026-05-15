@echo off
cd C:\Projects\wedding-weather-pipeline
call venv\Scripts\activate.bat
python main.py >> logs\pipeline.log 2>&1