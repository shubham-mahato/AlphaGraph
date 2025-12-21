export type ShockImpact = {
  node_id: string;
  node_type: string;
  distance: number;
  impact_score: number;
};

export type ShockResponse = {
  event_id: string;
  base_sentiment: number;
  impacts: ShockImpact[];
};