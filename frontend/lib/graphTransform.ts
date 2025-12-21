import { GraphResponse } from "@/types/graph";

export function toCytoscapeElements(graph: GraphResponse) {
  const nodes = graph.nodes.map((n) => {
    let color = "#64748b"; // Default Slate
    if (n.label === "Company") color = "#2563eb"; // Blue
    if (n.label === "Sector") color = "#059669";  // Emerald
    if (n.label === "Event") {
      const sentiment = n.properties.sentiment || 0;
      color = sentiment > 0 ? "#16a34a" : sentiment < 0 ? "#dc2626" : "#ca8a04";
    }

    return {
      data: {
        id: n.id,
        label: n.label,
        color: color,
        ...n.properties,
      },
    };
  });

  const edges = graph.edges.map((e, idx) => ({
    data: {
      id: `e-${idx}`,
      source: e.source,
      target: e.target,
      label: e.type,
    },
  }));

  return [...nodes, ...edges];
}