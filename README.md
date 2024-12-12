# X-Twitter Bot 🤖🐦

## Overview
A dynamic, scalable Twitter bot with advanced interaction capabilities.

## Features
- Multi-account management
- Intelligent tweet scheduling
- Sentiment-based interactions
- Magic UI dashboard

## Setup

### Prerequisites
- Python 3.9+
- Twitter Developer Account

### Installation
```bash
git clone https://github.com/yourusername/x-twitter-bot.git
cd x-twitter-bot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration
1. Create `.env` file
2. Add Twitter API credentials
3. Configure bot settings

## Running the Bot
```bash
uvicorn backend.main:app --reload
```

## Contributing
Check `FEATURES.md` for current status and roadmap.

## License
MIT License
