from pydantic import BaseModel, Field

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
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=10, ge=1, le=100)

class SearchResult(BaseModel):
    candidate: Candidate
    score: float

class DebugInfo(BaseModel):
    parsed_icp: dict
    hyde_profile: str
    filters_applied: dict
    candidates_after_metadata_filter: int
    returned: int

class SearchResponse(BaseModel):
    results: list[SearchResult]
    debug: DebugInfo   