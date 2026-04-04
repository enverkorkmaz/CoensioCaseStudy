import type { SearchResult } from "../types/candidate";
import CandidateCard from "./CandidateCard";

interface CandidateListProps {
  results: SearchResult[];
}

export default function CandidateList({ results }: CandidateListProps) {
  if (results.length === 0) return null;

  return (
    <div className="flex flex-col gap-4">
      <p className="text-sm text-gray-500">{results.length} aday bulundu</p>
      {results.map((result, index) => (
        <CandidateCard key={result.candidate.id} result={result} rank={index + 1} />
      ))}
    </div>
  );
}