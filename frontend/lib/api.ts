import axios from "axios";
import { GraphResponse } from "@/types/graph";

const BASE_URL = "http://localhost:8000";

export const api = axios.create({
  baseURL: BASE_URL,
});

export async function fetchCompanyGraph(ticker: string): Promise<GraphResponse> {
  try {
    const { data } = await api.get<GraphResponse>(`/graph/company/${ticker}`);
    return data;
  } catch (error) {
    console.error("Failed to fetch graph:", error);
    throw error;
  }
}