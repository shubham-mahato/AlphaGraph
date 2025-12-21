
export type SelectedNode = {
  id: string;
  label: string;
  title?: string;
  description?: string;
  sentiment?: number;
  timestamp?: string;
  event_id?: string; // Explicitly added for the simulation button
  [key: string]: unknown;
};

type Props = {
  node: SelectedNode | null;
  onSimulate?: (eventId: string) => void; // <--- NEW PROP ADDED
};

export default function NodeDetails({ node, onSimulate }: Props) {
  if (!node) {
      return (
        <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg text-gray-500 text-sm text-center h-[600px] flex items-center justify-center">
          Click a node to view details
        </div>
      );
    }
  
    const isEvent = node.label === "Event";
  
    return (
      <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm h-[600px] overflow-y-auto">
        <div className="mb-4">
          <span className={`text-xs font-bold uppercase px-2 py-1 rounded text-white ${
            node.label === "Company" ? "bg-blue-600" : isEvent ? "bg-red-500" : "bg-green-600"
          }`}>
            {node.label}
          </span>
        </div>
        
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          {node.title || node.id}
        </h2>
  
        {node.description && (
          <p className="text-gray-600 text-sm leading-relaxed mb-4">
            {node.description}
          </p>
        )}

        {/* ✅ NEW: SHOCK SIMULATION BUTTON */}
        {isEvent && onSimulate && (
          <button
            onClick={() => onSimulate(node.event_id as string || node.id)}
            className="w-full mb-6 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded transition-all shadow-md flex items-center justify-center gap-2"
          >
            <span>⚡ Run Shock Simulation</span>
          </button>
        )}
  
        <div className="space-y-2 text-sm border-t pt-4">
          {node.sentiment !== undefined && (
            <div className="flex justify-between">
              <span className="text-gray-500">Sentiment Score:</span>
              <span className={`font-mono font-bold ${Number(node.sentiment) > 0 ? "text-green-600" : "text-red-600"}`}>
                {Number(node.sentiment).toFixed(2)}
              </span>
            </div>
          )}
          
          {node.timestamp && (
              <div className="flex justify-between">
                  <span className="text-gray-500">Date:</span>
                  <span className="text-gray-900">{new Date(node.timestamp).toLocaleDateString()}</span>
              </div>
          )}
        </div>
      </div>
    );
}