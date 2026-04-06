from models import SearchRequest, SearchResponse, SearchResult
from services.embedding import get_embedding
from services.qdrant_service import search_candidates
from services.icp_service import parse_query

class CandidateService:
    @staticmethod
    def search(request: SearchRequest) -> SearchResponse:
        print(f"\n[Arama] Sorgu: '{request.query}' | Top K: {request.top_k}")

        
        icp = parse_query(request.query)
        print(f"[ICP] Parse sonucu: {icp}")

        
        search_text = icp.get("search_text") or request.query
        query_embedding = get_embedding(search_text)

        
        filters = {
            "location": icp.get("location"),
            "min_experience": icp.get("min_experience"),
            "university": icp.get("university")
        }

        
        all_results = search_candidates(query_embedding, 100, filters)
        before_skill_filter = len(all_results)

        
        icp_skills = [s.lower() for s in icp.get("skills", [])]
        if icp_skills:
            all_results = [
                r for r in all_results
                if any(s.lower() in icp_skills for s in r.candidate.skills)
            ]

        
        results = all_results[:request.top_k]

        
        debug = {
            "parsed_icp": icp,
            "search_text_used": search_text,
            "filters_applied": {k: v for k, v in filters.items() if v},
            "skill_filter": icp_skills if icp_skills else None,
            "candidates_after_metadata_filter": before_skill_filter,
            "candidates_after_skill_filter": len(all_results),
            "returned": len(results)
        }

        return SearchResponse(results=results, debug=debug)
