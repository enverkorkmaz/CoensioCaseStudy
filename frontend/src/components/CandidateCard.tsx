import type { SearchResult } from "../types/candidate";

interface CandidateCardProps {
  result: SearchResult;
  rank: number;
}

export default function CandidateCard({ result, rank }: CandidateCardProps) {
  const { candidate, score } = result;
  const matchPercent = Math.round(score * 100);

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="w-8 h-8 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-sm font-bold">
            {rank}
          </span>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{candidate.name}</h3>
            <p className="text-sm text-gray-500">{candidate.title}</p>
          </div>
        </div>
        <span className="text-sm font-medium text-green-600 bg-green-50 px-2 py-1 rounded-md">
          %{matchPercent} eşleşme
        </span>
      </div>

      <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-3">
        <span>📍 {candidate.location}</span>
        <span>💼 {candidate.experience_years} yıl deneyim</span>
        <span>🎓 {candidate.university}</span>
      </div>

      <div className="flex flex-wrap gap-1.5">
        {candidate.skills.map((skill) => (
          <span
            key={skill}
            className="px-2.5 py-1 bg-gray-100 text-gray-700 text-xs rounded-full font-medium"
          >
            {skill}
          </span>
        ))}
      </div>
      <div className="flex flex-wrap gap-1.5">
        <p className="mt-3 text-sm text-gray-500">
        {candidate.summary}
      </p>
      </div>

      <div className="mt-3 pt-3 border-t border-gray-100 text-xs text-gray-400 font-mono">
        Cosine Similarity: {score.toFixed(4)}
      </div>
    </div>
  );
}