# Wedding Weather Pipeline

A personal data engineering & ML project ingesting historical hourly weather data 
for Upminster, London from three sources (Meteostat, Open-Meteo, Visual Crossing) 
into Google BigQuery to forecast the weather on D-DAY.

## Stack
- Python 3.13
- Google BigQuery
- Meteostat / Open-Meteo / Visual Crossing APIs

## Status
🚧 In progress


# Wedding Weather Pipeline

## 📋 Project Summary          ← non-technical, 3-4 sentences
## 🎯 Objective                ← what problem it solves
## 🏗️ Architecture Overview    ← simple diagram, plain English
## 📊 Data Sources             ← what, where, coverage
## 🔄 Pipeline Layers          ← Bronze/Silver/ML in plain English
## ⚙️ Technical Stack          ← full stack list
## 🗂️ Repository Structure     ← folder structure
## 📈 Status                   ← per layer status table
## 🚀 Setup Guide              ← how to reproduce
## 📝 Design Decisions         ← why you made key choices

Why 3 data sources
Why medallion architecture
Why Silver preserves NULLs
Why separate ref dataset
Why MLflow over Vertex Experiments
Why Cloud Run for retraining