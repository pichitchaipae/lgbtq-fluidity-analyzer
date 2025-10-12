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
  timeout: 30000, // เพิ่มจาก 10s -> 30s สำหรับ AI chatbot (อาจใช้เวลานาน)
  headers: {
    'Content-Type': 'application/json; charset=utf-8', // เพิ่ม charset=utf-8 สำหรับภาษาไทย
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
  try {
    const { data } = await apiClient.post<ChatResponse>('/api/chatbot', payload);
    return data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Chatbot API error:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        payload: payload,
      });
      
      // ถ้า timeout หรือ network error ให้ลองใหม่อีกครั้ง
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        console.log('Timeout detected, retrying with longer timeout...');
        const retryClient = axios.create({
          baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
          timeout: 60000, // 60 วินาทีสำหรับ retry
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
          },
        });
        const { data } = await retryClient.post<ChatResponse>('/api/chatbot', payload);
        return data;
      }
      
      throw new Error(error.response?.data?.detail || error.message);
    }
    throw error;
  }
};
