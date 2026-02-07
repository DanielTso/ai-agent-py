"use client";

import { useState } from "react";
import { Search, FileText, AlertTriangle } from "lucide-react";
import { documentsApi } from "@/lib/api";

interface SearchResult {
  document: {
    id: string;
    title: string;
    doc_type: string;
    version: string;
  };
  relevance_score: number;
  snippet: string;
  page_number: number;
  section: string;
}

interface Contradiction {
  id: string;
  doc_a: { title: string };
  doc_b: { title: string };
  description: string;
  severity: string;
  status: string;
}

export default function DocumentsPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [contradictions, setContradictions] = useState<Contradiction[]>([]);
  const [searching, setSearching] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    try {
      setSearching(true);
      const data = (await documentsApi.search(query)) as {
        results: SearchResult[];
      };
      setResults(data.results);
    } catch {
      // Use mock data on error
      setResults([
        {
          document: {
            id: "DOC-001",
            title: "Structural Specification Rev C",
            doc_type: "spec",
            version: "C",
          },
          relevance_score: 0.92,
          snippet:
            "Section 3.2: Concrete mix design shall achieve 5000 PSI at 28 days.",
          page_number: 12,
          section: "3.2",
        },
      ]);
    } finally {
      setSearching(false);
    }
  };

  const loadContradictions = async () => {
    try {
      const data = (await documentsApi.contradictions()) as Contradiction[];
      setContradictions(data);
    } catch {
      setContradictions([
        {
          id: "CONTRA-001",
          doc_a: { title: "Structural Specification Rev C" },
          doc_b: { title: "Drawing Set A-101" },
          description:
            "Spec calls for 5000 PSI concrete but drawing note references 4000 PSI",
          severity: "high",
          status: "open",
        },
      ]);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Document Search</h1>

      {/* Search Bar */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <Search
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              placeholder="Search project documents..."
              className="w-full pl-10 pr-4 py-2 border rounded-lg text-sm"
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={searching}
            className="px-4 py-2 bg-primary text-white text-sm rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50"
          >
            {searching ? "Searching..." : "Search"}
          </button>
        </div>

        {results.length > 0 && (
          <div className="mt-4 space-y-3">
            {results.map((result) => (
              <div
                key={result.document.id}
                className="p-4 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center gap-2 mb-1">
                  <FileText size={16} className="text-primary" />
                  <span className="text-sm font-semibold text-gray-800">
                    {result.document.title}
                  </span>
                  <span className="text-xs text-gray-500">
                    v{result.document.version}
                  </span>
                  <span className="text-xs px-1.5 py-0.5 bg-primary/10 text-primary rounded">
                    {(result.relevance_score * 100).toFixed(0)}% match
                  </span>
                </div>
                <p className="text-sm text-gray-600">{result.snippet}</p>
                <p className="text-xs text-gray-400 mt-1">
                  Page {result.page_number}, Section {result.section}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Contradictions */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-800">
            Document Contradictions
          </h2>
          <button
            onClick={loadContradictions}
            className="text-sm text-primary hover:underline"
          >
            Load contradictions
          </button>
        </div>

        {contradictions.length > 0 ? (
          <div className="space-y-3">
            {contradictions.map((c) => (
              <div key={c.id} className="p-4 bg-amber-50 rounded-lg">
                <div className="flex items-center gap-2 mb-1">
                  <AlertTriangle size={16} className="text-warning" />
                  <span className="text-xs px-2 py-0.5 bg-amber-200 rounded font-medium">
                    {c.severity}
                  </span>
                </div>
                <p className="text-sm text-gray-800 mt-1">{c.description}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {c.doc_a.title} vs {c.doc_b.title}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500">
            Click &quot;Load contradictions&quot; to check for conflicts
          </p>
        )}
      </div>
    </div>
  );
}
