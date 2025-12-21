export type GraphNode = {
  id: string;
  label: "Company" | "Sector" | "Event";
  properties: {
    title?: string;
    description?: string;
    sentiment?: number;
    ticker?: string;
    name?: string;
    [key: string]: string | number | boolean | null | undefined;
  };
};

export type GraphEdge = {
  source: string;
  target: string;
  type: string;
};

export type GraphResponse = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};