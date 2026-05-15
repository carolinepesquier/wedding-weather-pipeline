@echo off
cd C:\Users\pesquic\wedding-weather-pipeline
venv\Scripts\python.exe vc_backfill_scheduled.py >> logs\vc_backfill.log 2>&1