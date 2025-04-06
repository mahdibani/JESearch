# JESearch

# JESearch - Junior Enterprise Intelligence Platform 🔍✨

[![GitHub License](https://img.shields.io/github/license/mahdibani/JESearch)](LICENSE)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-%23009688)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React-%2361DAFB)](https://react.dev)
[![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter.ai-%234B32C3)](https://openrouter.ai)

A comprehensive platform for discovering, analyzing, and collaborating with Junior Enterprises worldwide using AI-powered insights.

## Demo 🎥

https://drive.google.com/file/d/1ULzOL3ofJYvA8ChYBuVsc5Q4WlsJoTby/view?usp=sharing

## Features 🌟

- 🕵️ **Smart Search**: Natural language search across JE databases
- 🤝 **Compatibility Analysis**: AI-driven similarity scoring (TF-IDF + Cosine)
- 📧 **Auto-generated Proposals**: Context-aware collaboration emails
- 🌍 **Global Directory**: JE profiles with social media integration
- 📊 **Interactive Dashboard**: Visual comparison and recommendations

## Architecture 🏗️

![Image](https://github.com/user-attachments/assets/d11efaa1-1744-431e-abd9-0b546ea79763)

## Installation & Setup ⚡

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API key (via OpenRouter)

### Backend Services
```bash
# Set up Python environment
cd Backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run all services (3 terminals)
python search_service.py    # Port 8008
python compare_service.py   # Port 8099 
python generate_service.py  # Port 8066

Usage Guide 🚀
Search Interface

Enter natural language queries (e.g., "Marketing JEs in France")

Browse interactive cards with key JE information

Comparison Engine

Click "Compare" on any JE card

View real-time similarity score and AI recommendations

Analyze service overlaps and potential synergies

Collaboration Generator

From comparison results, click "Generate Message"

Customize and copy AI-drafted collaboration proposal

Directly contact JEs using provided social links

Tech Stack 🔧
Component	Technology
Frontend	React, Vite, Axios
Backend	FastAPI, Uvicorn
AI/ML	Llama-3-70B, TF-IDF, Cosine Sim
NLP	OpenRouter.ai API
Data Processing	Scikit-learn, Pandas
