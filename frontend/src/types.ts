export type SurveyAnswers = {
  media1: number;
  media2: number;
  family1: number;
  family2: number;
  family3: number;
  community1: number;
  community2: number;
  culture1: number;
  culture2: number;
  exploration1: number;
  exploration2: number;
  school1: number;
};

export type SectionScore = {
  raw_score: number;
  max_score: number;
  percentage: number;
  weight: number;
};

export type AnalysisResponse = {
  timestamp: string;
  overall_score: number;
  interpretation: {
    level: string;
    description: string;
    emoji: string;
    range: string;
  };
  section_scores: Record<string, SectionScore>;
  insights: string[];
  disclaimer: string;
  references: string[];
};

// Types for v2 Analysis
export interface AnalysisV2Request {
  dataset: AnalysisRequest[];
  ai_insights: boolean;
  language: 'th' | 'en';
}

export interface AnovaResults {
  [key: string]: {
    sum_of_squares: number;
    df: number;
    F: number;
    p_value: number;
    eta_sq?: number;
  };
}

export interface Visualizations {
  interaction_plot: {
    [key: string]: { [key: string]: number };
  };
  group_means: {
    [key: string]: number;
  };
}

export interface AnalysisV2Response {
  anova_results: AnovaResults;
  ai_interpretation: string | null;
  visualizations: Visualizations;
  privacy_notice: string;
}
