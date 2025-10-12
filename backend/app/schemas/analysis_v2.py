from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AnalysisV2Request(BaseModel):
    """Request schema for v2 analysis."""
    dataset: List[Dict[str, int]] = Field(..., description="List of survey responses.")
    ai_insights: bool = Field(default=True, description="Whether to include AI-powered insights.")
    language: str = Field(default="th", description="Language for the AI interpretation (th/en).")

class AnalysisV2Response(BaseModel):
    """Response schema for v2 analysis."""
    anova_results: Dict[str, Any]
    ai_interpretation: str | None = None
    visualizations: Dict[str, Any]
    privacy_notice: str