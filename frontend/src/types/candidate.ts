export interface Candidate {
  id: number;
  name: string;
  title: string;
  location: string;
  experience_years: number;
  skills: string[];
  university: string;
  department: string;
  summary: string;
}

export interface SearchResult {
  candidate: Candidate;
  score: number;
}

export interface SearchResponse {
  results: SearchResult[];
  debug: {
    parsed_icp: Record<string, unknown>;
    search_text_used: string;
    filters_applied: Record<string, unknown>;
    skill_filter: string[] | null;
    candidates_after_metadata_filter: number;
    candidates_after_skill_filter: number;
    returned: number;
  };
}