import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import SearchRequest, SearchResponse
from services.candidate_service import CandidateService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(title="Aday Arama Sistemi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    return CandidateService.search(request)
