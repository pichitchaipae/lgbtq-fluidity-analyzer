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
