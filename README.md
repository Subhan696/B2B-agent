# Zero-Budget B2B Lead Magnet Agent

An autonomous agent that researches companies and generates personalized outreach using free tools.

## Tech Stack
- **Backend**: Python (FastAPI), DuckDuckGo Search, Playwright, Gemini 1.5 Flash.
- **Frontend**: Next.js 15, TailwindCSS, Shadcn/UI (Simulated).

## Setup

### Prerequisites
- Node.js & npm
- Python 3.9+
- Gemini API Key (Get free from [Google AI Studio](https://aistudio.google.com/))

### Backend
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows)
4. `pip install -r requirements.txt` (or install manually)
5. `playwright install`
6. Create `.env` file with `GEMINI_API_KEY=your_key`
7. Run: `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Usage
Open `http://localhost:3000`, enter a domain (e.g., `stripe.com`), and watch the agent research.
