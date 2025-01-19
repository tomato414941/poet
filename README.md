# Poet

A philosophical thinking system that generates thoughts and contemplations.

🌐 **Live Demo**: [poet.up.railway.app](https://poet.up.railway.app)

## Features

- **Chain of Thoughts**: Each new thought builds upon the previous one
- **RESTful API**: Easy integration with other systems through a FastAPI-based REST API
- **Automatic Generation**: Generates new thoughts every 10 minutes
- **Natural Language**: Outputs thoughts in natural Japanese language
- **Modern Web Interface**: Clean and responsive UI built with Tailwind CSS

## Architecture

### Backend
- Python 3.8+
- FastAPI for API endpoints
- LangChain + OpenAI API for thought generation
- Asynchronous processing for non-blocking operations

### Frontend
- HTML5 + JavaScript
- Tailwind CSS for styling
- Responsive design
- Error handling and debugging capabilities

### API Endpoints

```
GET /thoughts
Get the history of all thoughts

GET /thoughts/latest
Get the most recent thought
```

The system automatically starts generating thoughts when the server starts, creating a new thought every 10 minutes.

## Project Structure

```
poet/
├── config/                 # Configuration files
│   ├── api_keys.py        # API keys (not in version control)
│   ├── api_keys.py.template # Template for API keys
│   └── prompts.py         # System prompts and default settings
├── poet/                  # Main package
│   ├── api.py            # FastAPI application and endpoints
│   └── poet.py           # Core Poet class for thought generation
├── static/               # Frontend files
│   ├── index.html       # Main HTML file
│   └── js/             # JavaScript files
│       └── main.js     # Frontend logic
├── tests/               # Test files
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── requirements.txt     # Python dependencies
└── run_api.py          # Script to run the FastAPI server
```

## Setup

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Copy the environment variables template
cp .env.example .env

# Edit .env and add your OpenAI API key
```

4. Start the server:
```bash
python run_api.py
```

The API will be available at `http://localhost:8000`. You can view the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

The web interface will be available at `http://localhost:8000`.

## Environment Variables

The following environment variables can be set in `.env` file or in your environment:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `APP_ENV`: Application environment (default: development)
- `DEBUG`: Enable debug mode (default: true)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

For production deployment, it's recommended to:
1. Set these variables in your deployment environment
2. Set `DEBUG=false` and `APP_ENV=production`
3. Use appropriate `HOST` and `PORT` settings for your environment
