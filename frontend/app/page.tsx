"use client";

import { useState } from "react";
import { fetchCompanyGraph } from "@/lib/api";
import { toCytoscapeElements } from "@/lib/graphTransform";
import GraphView from "@/components/GraphView";
import SearchBar from "@/components/SearchBar";
import NodeDetails, { SelectedNode } from "@/components/NodeDetails"; 
import { ElementDefinition } from "cytoscape";

export default function Home() {
  const [elements, setElements] = useState<ElementDefinition[]>([]);
  
 
  const [selectedNode, setSelectedNode] = useState<SelectedNode | null>(null);
  
  const [loading, setLoading] = useState(false);

  const handleSearch = async (ticker: string) => {
    if (!ticker) return;
    setLoading(true);
    try {
      const graph = await fetchCompanyGraph(ticker);
      setElements(toCytoscapeElements(graph) as ElementDefinition[]);
      setSelectedNode(null);
    } catch (err) {
      console.error(err);
      alert("Company not found or API error. Check backend console.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">
            AlphaGraph <span className="text-blue-600">Intelligence</span>
          </h1>
          <p className="text-gray-500 mt-2">
            Real-time Knowledge Graph for Financial Events
          </p>
        </header>

        <SearchBar onSearch={handleSearch} />

        {loading ? (
          <div className="text-center py-20 text-gray-500 animate-pulse">
            Loading Knowledge Graph...
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <GraphView 
                elements={elements} 
                onNodeClick={(data) => setSelectedNode(data as SelectedNode)} 
              />
            </div>
            <div className="lg:col-span-1">
              <NodeDetails node={selectedNode} />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}