import logging
from models import SearchRequest, SearchResponse, SearchResult, DebugInfo
from services.embedding import get_embedding
from services.qdrant_service import search_candidates
from services.icp_service import parse_query, generate_hypothetical_candidate

logger = logging.getLogger(__name__)

class CandidateService:
    @staticmethod
    def search(request: SearchRequest) -> SearchResponse:
        logger.info(f"Arama başladı: '{request.query}' | top_k={request.top_k}")

        icp = parse_query(request.query)
        logger.info(f"ICP: {icp}")

        hyde_profile = generate_hypothetical_candidate(request.query)
        query_embedding = get_embedding(hyde_profile)

        filters = {
            "location": icp.get("location"),
            "min_experience": icp.get("min_experience"),
            "university": icp.get("university")
        }

        all_results = search_candidates(query_embedding, 100, filters)
        results = all_results[:request.top_k]

        debug = DebugInfo(
            parsed_icp=icp,
            hyde_profile=hyde_profile,
            filters_applied={k: v for k, v in filters.items() if v},
            candidates_after_metadata_filter=len(all_results),
            returned=len(results)
        )

        logger.info(f"Arama tamamlandı: {len(results)} aday döndürüldü")
        return SearchResponse(results=results, debug=debug)
