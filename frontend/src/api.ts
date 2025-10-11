import axios from "axios";

import type { AnalysisResponse, SurveyAnswers } from "./types";

// Use relative path when in production (nginx will proxy to backend)
// Use localhost:8000 for local development
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "/api/v1",
  timeout: 10000,
});

export const analyzeSurvey = async (answers: SurveyAnswers): Promise<AnalysisResponse> => {
  const { data } = await api.post<AnalysisResponse>('/analysis', answers);
  return data;
};
