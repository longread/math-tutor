# Math Tutor AI

An AI-powered math tutoring application that provides step-by-step solutions to math problems.

## Features

- Text-based math problem solving
- Image upload support for handwritten or photographed problems
- Step-by-step explanations with LaTeX formatting
- **Multi-LLM Support**: Choose between OpenAI GPT-4o or Google Gemini
- Configurable via environment variables

## Supported LLM Providers

- **OpenAI GPT-4o** (default)
- **Google Gemini 2.0 Flash**

## Local Development

### Prerequisites

- Python 3.8+
- API key for your chosen LLM provider:
  - OpenAI API key (for GPT-4o), OR
  - Google API key (for Gemini)

### Installation

1. Clone the repository

2. Install dependencies:
```bash
pip install -e .
```

3. Create a `.env` file with your configuration:

**For OpenAI (default):**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

**For Google Gemini:**
```bash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_google_api_key_here
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. Open your browser to `http://localhost:8000`

## Deployment to Google Cloud Run

### Prerequisites

1. Google Cloud account
2. Google Cloud CLI (`gcloud`) installed

### Deploy

1. Set your project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

2. Build and deploy:

**With OpenAI:**
```bash
gcloud run deploy math-tutor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars LLM_PROVIDER=openai,OPENAI_API_KEY=your_openai_key
```

**With Google Gemini:**
```bash
gcloud run deploy math-tutor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars LLM_PROVIDER=gemini,GOOGLE_API_KEY=your_google_key
```

3. Access your application at the URL provided by Cloud Run

## Technology Stack

- **Backend**: FastAPI
- **AI**: OpenAI GPT-4o / Google Gemini 2.0 Flash (configurable)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Google Cloud Run

## Architecture

The application uses a **factory pattern** for LLM providers:

```
app/
├── llm_models/           # LLM provider package
│   ├── base.py          # Abstract base class
│   ├── openai_provider.py   # OpenAI implementation
│   ├── gemini_provider.py   # Gemini implementation
│   └── factory.py       # Provider factory
├── ai_service.py        # Main AI service (uses factory)
├── main.py              # FastAPI application
└── parser.py            # Response parser
```

## Switching LLM Providers

Simply change the `LLM_PROVIDER` environment variable:

```bash
# Use OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_key

# OR use Gemini
export LLM_PROVIDER=gemini
export GOOGLE_API_KEY=your_key
```

No code changes required!

