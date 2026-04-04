from pydantic import BaseModel

class Candidate(BaseModel):
    id: int
    name: str
    title: str
    location: str
    experience_years: int
    skills: list[str]
    university: str
    department: str
    summary: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 10

class SearchResult(BaseModel):
    candidate: Candidate
    score: float        

class SearchResponse(BaseModel):
    results: list[SearchResult]
    debug: dict   