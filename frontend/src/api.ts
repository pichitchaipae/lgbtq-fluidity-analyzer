import axios from "axios";

import type { 
  AnalysisResponse, 
  AnalysisRequest, 
  AnalysisV2Request, 
  AnalysisV2Response,
  ChatRequest,
  ChatResponse 
} from "./types";

// Use relative path when in production (nginx will proxy to backend)
// Use localhost:8000 for local development
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeSurvey = async (answers: AnalysisRequest): Promise<AnalysisResponse> => {
  const { data } = await apiClient.post<AnalysisResponse>('/api/v1/analysis', answers);
  return data;
};

export const analyzeDatasetV2 = async (payload: AnalysisV2Request): Promise<AnalysisV2Response> => {
  const { data } = await apiClient.post<AnalysisV2Response>('/api/v2/analysis', payload);
  return data;
};

export const chatbot = async (payload: ChatRequest): Promise<ChatResponse> => {
  const { data } = await apiClient.post<ChatResponse>('/api/chatbot', payload);
  return data;
};
