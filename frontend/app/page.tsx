"use client";

import { useState } from "react";
import { fetchCompanyGraph, fetchShockSimulation } from "@/lib/api"; // Import new API
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
      alert("Company not found or API error.");
    } finally {
      setLoading(false);
    }
  };

  // ✅ NEW: Handle the Simulation Logic
  const handleSimulate = async (eventId: string) => {
    try {
        const response = await fetchShockSimulation(eventId);
        
        // Create a map for O(1) lookup: "TCS" -> -0.45
        const impactMap = new Map(response.impacts.map(i => [i.node_id, i.impact_score]));

        // Update elements with new colors
        setElements((prevElements) => 
            prevElements.map((el) => {
                const nodeId = el.data.id as string;
                if (impactMap.has(nodeId)) {
                    const score = impactMap.get(nodeId) || 0;
                    // Color Logic: Red for negative, Green for positive
                    // Opacity Logic: Stronger score = Darker color
                    const color = score < 0 ? "#ef4444" : "#22c55e"; // Red-500 or Green-500
                    
                    return {
                        ...el,
                        data: {
                            ...el.data,
                            color: color, // Override color
                            // Optional: Add a border to highlight affected nodes
                            borderWidth: 4, 
                            borderColor: "#000"
                        }
                    };
                }
                return el;
            })
        );
        alert(`Simulation Complete! Affected ${response.impacts.length} companies.`);
    } catch (e) {
        alert("Simulation failed.");
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
              {/* Pass the handler to the component */}
              <NodeDetails 
                node={selectedNode} 
                onSimulate={handleSimulate} 
              />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}