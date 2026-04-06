# AI Candidate Search System

This project is an AI-powered candidate search and matching system. It allows companies to find the most suitable candidates for their open positions using natural language queries. Users can type queries in everyday language, such as *"Senior React Developer living in Istanbul with at least 3 years of experience"*. The system analyzes this query and lists the best candidates from the database by calculating semantic similarities.

## 🚀 Technologies & Architecture

The project is developed with a modern and scalable architecture:

- **Backend (API):** FastAPI, Python, Pydantic
- **AI & Semantic Search:** OpenAI (Embeddings & Completion API), Qdrant (Vector Database)
- **Frontend (User Interface):** React, TypeScript, Vite, Tailwind CSS
- **Infrastructure:** Docker & Docker Compose

## 🧠 How It Works

The system uses a **hybrid search** approach combining metadata filtering with semantic search:

1. **ICP Parsing (Bonus Feature):** The user's natural language query is sent to GPT-4o-mini, which extracts structured information — location, skills, years of experience, and university — as an Ideal Candidate Profile (ICP). This is the bonus feature mentioned in the case study.

2. **Metadata Filtering:** Hard constraints like location, experience, and university are applied as Qdrant payload filters to narrow down the candidate pool.

3. **Semantic Search:** The remaining free-text portion of the query is converted into a 1536-dimensional vector using OpenAI's `text-embedding-3-small` model. Qdrant performs cosine similarity search within the filtered pool.

4. **Skill Filtering:** Skills extracted by ICP are used for case-insensitive post-filtering in Python (dual representation — skills are also included in the semantic search text).

## 📁 Project Structure

```
CoensioCaseStudy/
├── docker-compose.yml              # All services (Qdrant, Backend, Frontend)
├── NOTLAR.md                        # Technical notes (RAG, Vector DB vs SQL, improvements)
├── README.md                        # Setup & usage instructions
│
├── backend/
│   ├── .env                         # OpenAI API key (not tracked by git)
│   ├── Dockerfile                   # Backend container definition
│   ├── requirements.txt             # Python dependencies
│   ├── config.py                    # Central configuration (API keys, Qdrant settings)
│   ├── models.py                    # Pydantic models (Candidate, SearchRequest, etc.)
│   ├── main.py                      # FastAPI app — API endpoints, search orchestration
│   ├── seed.py                      # Database seeder — 10 demo candidates
│   └── services/
│       ├── embedding.py             # OpenAI text → vector conversion
│       ├── icp_service.py           # GPT-powered query parsing (ICP - bonus)
│       ├── qdrant_service.py        # Qdrant operations (create, upsert, search)
        └── candidate_service.py     # Candidate search 
│
└── frontend/
    ├── Dockerfile                   # Frontend container (multi-stage: build + nginx)
    ├── index.html                   # HTML entry point
    ├── package.json                 # Node dependencies
    ├── vite.config.ts               # Vite configuration
    ├── tailwind.config.js           # Tailwind CSS configuration
    └── src/
        ├── main.tsx                 # React entry point
        ├── App.tsx                  # Main component — search logic, API calls
        ├── index.css                # Tailwind imports
        ├── types/
        │   └── candidate.ts         # TypeScript interfaces
        └── components/
            ├── SearchBar.tsx         # Search input + button
            ├── CandidateCard.tsx     # Single candidate result card
            └── CandidateList.tsx     # List of candidate cards
```

## 📋 Prerequisites

To run the project on your machine, you need to have the following installed:
- Node.js (v22+)
- Python (v3.12+)
- Docker Desktop (or Docker Engine & Docker Compose)
- A valid OpenAI API Key

## 🛠️ Setup Instructions

You can start the project easily using Docker, or set it up manually.

### One-Click Setup (Full Docker Installation - Recommended)

You can use the `docker-compose.yml` file in the root directory to spin up the Backend, Frontend, and Qdrant database all at once.

First, create a `.env` file inside the `backend` folder and add your OpenAI key:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

Then, start all services in the root directory:
```bash
docker compose up -d --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Qdrant: `http://localhost:6333`

> **Important Note (For First Setup Only):** After the system is up and running, you need to populate the database with dummy candidates (seeding):
> ```bash
> docker compose exec backend python seed.py
> ```
> *Once the data is added, the system is fully ready to use!*

---

### Manual Setup (Alternative)

If you want to use Docker only for the database (Qdrant) and run the Backend and Frontend independently on your host machine, follow these steps.

#### 1. Running Only the Database (Qdrant)

```bash
docker compose up -d qdrant
```

#### 2. Backend Setup & Seeding

```bash
cd backend

# Create and activate virtual environment (Windows):
python -m venv venv
venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt
```

Create a `.env` file in the backend folder:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

Seed the database and start the server:
```bash
python seed.py
uvicorn main:app --reload
```
*Backend API: `http://localhost:8000` | Swagger UI: `http://localhost:8000/docs`*

#### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
*Frontend: `http://localhost:5173`*

## 💡 Usage

Open the frontend interface and type a query in natural language into the search bar.

**Example Queries:**
- *"Software developers who know React and live in Istanbul"*
- *"A university graduate Python developer with at least 5 years of experience"*
- *"Junior Data Scientists in Ankara"*
- *"TypeScript bilen frontend developer"*
- *"Bilkent mezunu Docker bilen"*

The system will parse the Ideal Candidate Profile (ICP) from your sentence using GPT-4o-mini, apply metadata filters (location, experience, university) on Qdrant, run semantic search with cosine similarity, and present the most relevant candidates.

## 📝 Technical Notes

See [NOTLAR.md](NOTLAR.md) for detailed technical notes covering:
- What is RAG and how it was applied in this project
- Why vector databases over traditional SQL
- Architectural decisions and limitations
- Potential improvements (multi-embedding, HyDE, re-ranking, generation)
