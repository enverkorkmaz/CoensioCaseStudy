# AI Candidate Search System

This project is an AI-powered candidate search and matching system. It allows companies to find the most suitable candidates for their open positions using natural language queries. Users can type queries in everyday language, such as *"Senior React Developer living in Istanbul with at least 3 years of experience"*. The system analyzes this query (extracting the Ideal Candidate Profile - ICP) and lists the best candidates from the database by calculating semantic similarities.

## 🚀 Technologies & Architecture

The project is developed with a modern and scalable architecture:

- **Backend (API):** FastAPI, Python, Pydantic
- **AI & Semantic Search:** OpenAI (Embeddings & Completion API), Qdrant (Vector Database)
- **Frontend (User Interface):** React, TypeScript, Vite, Tailwind CSS
- **Infrastructure:** Docker & Docker Compose 

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

First, to use the API, make sure you create a `.env` file inside the `backend` folder and add your OpenAI key:
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

> **Important Note (For First Setup Only):** After the system is up and running, you need to populate the database with dummy candidates (seeding). You can run `seed.py` by sending a command to the backend container:
> ```bash
> docker compose exec backend python seed.py
> ```
> *Once the data is added, the system is fully ready to use!*

---

### Manual Setup (Alternative)

If you strictly want to use Docker for the database (Qdrant) and run the Backend and Frontend independently on your host machine, follow these steps in order.

#### 1. Running Only the Database (Qdrant)

```bash
docker compose up -d qdrant
```

#### 2. Backend Setup & Seeding

Go to the backend directory, install dependencies, and configure settings:

```bash
cd backend

# Create and activate virtual environment (Windows):
python -m venv venv
venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt
```

Create a `.env` file in the backend folder and add your OpenAI API key like this:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

Run the `seed.py` file to insert sample candidate data into the Qdrant database and perform embedding processes:
```bash
python seed.py
```

Start the FastAPI server:
```bash
uvicorn main:app --reload
```
*The Backend API will now be running at `http://localhost:8000`. You can access the Swagger UI documentation at `http://localhost:8000/docs`.*

#### 3. Frontend Setup

Open a new terminal, go to the frontend directory, and start the React application:

```bash
cd frontend

# Install dependencies:
npm install

# Start development server:
npm run dev
```
*You can usually access the application interface at `http://localhost:5173`. Please check the terminal output.*

## 💡 Usage

When using the system, open the frontend interface and type a query in natural language into the search bar.

**Example Queries:**
- *"Software developers who know React and live in Istanbul"*
- *"A university graduate Python developer with at least 5 years of experience"*
- *"Junior Data Scientists in Ankara"*

The system will use OpenAI to parse the Ideal Candidate Profile (Location, Skills, Years of Experience, University info, etc.) from your sentence and run a semantic search on Qdrant to present you with the most relevant candidates.

---
