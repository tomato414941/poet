# Poet

An autonomous thinking system.

## Overview

Poet is a system that autonomously generates thoughts and shares its thinking process through an API.

## Architecture

### Backend
- Python + FastAPI
- OpenAI API

### Frontend
- HTML + JavaScript
- Thought process visualization
- Simple interaction

## API

```
GET /api/thoughts
Get a list of thought processes

GET /api/thoughts/{id}
Get details of a specific thought process
```

## Requirements

- Python 3.8+
- FastAPI
- OpenAI API
- uvicorn

## Development Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn poet.main:app --reload
```

## License

MIT License
