"use client";
import CytoscapeComponent from "react-cytoscapejs";
import { ElementDefinition } from "cytoscape"; 

type NodeData = Record<string, unknown>;


type Props = {
  elements: ElementDefinition[]; 
  onNodeClick: (data: NodeData) => void;
};

export default function GraphView({ elements, onNodeClick }: Props) {
  return (
    <div className="border border-gray-200 rounded-lg shadow-sm bg-white overflow-hidden">
      <CytoscapeComponent
        elements={elements}
        style={{ width: "100%", height: "600px" }}
        layout={{ 
          name: "cose", 
          animate: true,
          nodeRepulsion: 8000, 
          idealEdgeLength: 100,
        }}
        stylesheet={[
          {
            selector: "node",
            style: {
              label: "data(id)",
              "background-color": "data(color)",
              color: "#333",
              "font-size": "12px",
              "text-valign": "bottom",
              "text-margin-y": 6,
              width: 40,
              height: 40,
              "border-width": 2,
              "border-color": "#fff",
            },
          },
          {
            selector: 'node[label = "Company"]',
            style: { width: 60, height: 60, "font-weight": "bold" }
          },
          {
            selector: "edge",
            style: {
              width: 2,
              "line-color": "#cbd5e1",
              "target-arrow-color": "#cbd5e1",
              "target-arrow-shape": "triangle",
              "curve-style": "bezier",
            },
          },
          {
            selector: ":selected",
            style: {
              "border-width": 4,
              "border-color": "#fbbf24",
            },
          }
        ]}
        cy={(cy) => {
          cy.on("tap", "node", (evt) => {
            const data = evt.target.data() as NodeData;
            onNodeClick(data);
          });
        }}
      />
    </div>
  );
}