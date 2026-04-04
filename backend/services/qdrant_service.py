from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue, MatchAny, Range
from config import QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME, EMBEDDING_DIMENSION
from models import Candidate, SearchResult

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def init_collection():
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)

    if exists:
        client.delete_collection(COLLECTION_NAME)
        print(f"[Qdrant] '{COLLECTION_NAME}' collection silindi")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIMENSION,
            distance=Distance.COSINE
        )
    )
    print(f"[Qdrant] '{COLLECTION_NAME}' collection oluşturuldu (boyut: {EMBEDDING_DIMENSION})")


def upsert_candidate(candidate: Candidate, embedding: list[float]):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=candidate.id,
                vector=embedding,
                payload={
                    "name": candidate.name,
                    "title": candidate.title,
                    "location": candidate.location,
                    "experience_years": candidate.experience_years,
                    "skills": candidate.skills,
                    "university": candidate.university,
                    "department": candidate.department,
                    "summary": candidate.summary
                }
            )
        ]
    )
    print(f"[Qdrant] Aday eklendi: {candidate.name}")


def search_candidates(query_embedding: list[float], top_k: int = 5, filters: dict = None) -> list[SearchResult]:
    query_filter = None

    if filters:
        conditions = []

        if filters.get("location"):
            conditions.append(
                FieldCondition(
                    key="location",
                    match=MatchValue(value=filters["location"])
                )
            )

        if filters.get("min_experience"):
            conditions.append(
                FieldCondition(
                    key="experience_years",
                    range=Range(gte=filters["min_experience"])
                )
            )
        if filters.get("university"):
            conditions.append(
                FieldCondition(
                    key="university",
                    match=MatchValue(value=filters["university"])
                )
            )
        if conditions:
            query_filter = Filter(must=conditions)

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        query_filter=query_filter,
        limit=top_k
    )

    search_results = []
    for point in results:
        candidate = Candidate(
            id=point.id,
            name=point.payload["name"],
            title=point.payload["title"],
            location=point.payload["location"],
            experience_years=point.payload["experience_years"],
            skills=point.payload["skills"],
            university=point.payload["university"],
            department=point.payload["department"],
            summary=point.payload["summary"]
        )
        search_results.append(SearchResult(candidate=candidate, score=round(point.score, 4)))

    print(f"[Qdrant] {len(search_results)} aday bulundu (filtre: {filters})")
    return search_results
  