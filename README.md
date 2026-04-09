# AI Candidate Search System

This project is an AI-powered candidate search and matching system. Users can type queries in natural language, such as *"Senior React Developer living in Istanbul with at least 3 years of experience"*. The system analyzes the query and lists the best matching candidates using semantic similarity.

## Technologies & Architecture

- **Backend:** FastAPI, Python, Pydantic
- **AI & Semantic Search:** OpenAI (Embeddings & Chat API), Qdrant (Vector Database)
- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Infrastructure:** Docker & Docker Compose

## How It Works

The system uses a pipeline combining ICP parsing, HyDE, metadata filtering, and semantic search:

1. **ICP Parsing:** The user's natural language query is sent to GPT-4o-mini, which extracts structured information — location, skills, years of experience, and university — as an Ideal Candidate Profile (ICP). This is the bonus feature mentioned in the case study.

2. **HyDE (Hypothetical Document Embeddings):** Instead of embedding the query directly, GPT-4o-mini generates a hypothetical candidate profile that matches the query. This profile is in the same format as real candidate summaries, so it produces much closer vectors in embedding space — significantly improving cosine similarity scores (from 0.20–0.50 to 0.70+).

3. **Metadata Filtering:** Hard constraints extracted by ICP (location, experience, university) are applied as Qdrant payload filters to narrow down the candidate pool.

4. **Semantic Search:** The HyDE embedding is used for cosine similarity search within the filtered pool. Skills are handled semantically through HyDE rather than as a hard filter.

## Project Structure

```
CoensioCaseStudy/
├── docker-compose.yml              # All services (Qdrant, Backend, Frontend)
├── NOTLAR.md                       # Technical notes (RAG, Vector DB vs SQL, improvements)
├── README.md                       # Setup & usage instructions
│
├── backend/
│   ├── .env                        # OpenAI API key (not tracked by git)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── config.py                   # Central configuration (API keys, Qdrant settings)
│   ├── models.py                   # Pydantic models (Candidate, SearchRequest, DebugInfo...)
│   ├── main.py                     # FastAPI app — endpoints, logging config
│   ├── seed.py                     # Database seeder — 10 demo candidates
│   └── services/
│       ├── candidate_service.py     # Search orchestration — ICP, HyDE, filters, results
│       ├── embedding.py             # OpenAI text → vector conversion
│       ├── icp_service.py           # ICP query parsing + HyDE profile generation
│       └── qdrant_service.py        # Qdrant operations (create, upsert, search)
│
└── frontend/
    ├── Dockerfile                  # Multi-stage: Node build + Nginx serve
    ├── index.html                  # HTML entry point
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    └── src/
        ├── main.tsx                # React entry point
        ├── App.tsx                 # Main component — search logic, API calls
        ├── index.css               # Tailwind imports
        ├── types/
        │   └── candidate.ts        # TypeScript interfaces
        └── components/
            ├── SearchBar.tsx
            ├── CandidateCard.tsx
            └── CandidateList.tsx
```

## Prerequisites

- Docker Desktop (or Docker Engine & Docker Compose)
- A valid OpenAI API Key

## Setup (Docker — Recommended)

Create a `.env` file inside the `backend` folder:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

Start all services:
```bash
docker compose up -d --build
```

Services start in order — Qdrant first, then backend (waits for Qdrant to be healthy), then frontend.

Seed the database (first time only):
```bash
docker compose exec backend python seed.py
```

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Qdrant: `http://localhost:6333`

## Setup (Manual)

#### 1. Start Qdrant
```bash
docker compose up -d qdrant
```

#### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Create `backend/.env`:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

```bash
python seed.py
uvicorn main:app --reload
```

#### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage

Open `http://localhost:5173` and type a natural language query.

**Example queries:**
- `İstanbul'da React bilen senior developer`
- `Ankara'da 3 yıl deneyimli Python backend developer`
- `ODTÜ mezunu DevOps engineer`
- `Boğaziçi'nden veri bilimci`
- `TypeScript bilen full stack developer`

## Technical Notes

See [NOTLAR.md](NOTLAR.md) for detailed technical notes covering:
- What is RAG and how it was applied in this project
- Why FastAPI and Qdrant were chosen
- Why vector databases over traditional SQL
- HyDE implementation and cosine similarity improvements
- Potential improvements (LLM re-ranking, multi-embedding, unit tests)