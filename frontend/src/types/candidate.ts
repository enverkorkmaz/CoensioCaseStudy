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

export interface DebugInfo {
  parsed_icp: Record<string, unknown>;
  hyde_profile: string;
  filters_applied: Record<string, unknown>;
  candidates_after_metadata_filter: number;
  returned: number;
}

export interface SearchResponse {
  results: SearchResult[];
  debug: DebugInfo;
}
