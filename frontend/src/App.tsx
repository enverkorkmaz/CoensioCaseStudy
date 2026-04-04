import { useState } from "react";
import type { SearchResponse, SearchResult } from "./types/candidate";
import SearchBar from "./components/SearchBar";
import CandidateList from "./components/CandidateList";

function App() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  const handleSearch = async (query: string) => {
    setLoading(true);
    setError("");
    setSearched(true);

   try {
      const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 10 }),
      });

      if (!response.ok) throw new Error("API hatası");

      const data: SearchResponse = await response.json();
      setResults(data.results);
    } catch {
      setError("Arama yapılırken bir hata oluştu. Backend çalışıyor mu?");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Aday Arama Sistemi
          </h1>
          <p className="text-gray-500">
            Doğal dilde arama yaparak en uygun adayları bulun
          </p>
        </div>

        <div className="mb-8">
          <SearchBar onSearch={handleSearch} loading={loading} />
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        {searched && !loading && results.length === 0 && !error && (
          <p className="text-center text-gray-400">Sonuç bulunamadı.</p>
        )}

        <CandidateList results={results} />
      </div>
    </div>
  );
}

export default App;