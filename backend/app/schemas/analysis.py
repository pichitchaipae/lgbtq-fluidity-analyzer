"""Pydantic schemas for the analysis API."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field, validator


class AnalysisRequest(BaseModel):
    media1: int = Field(..., ge=0, le=4)
    media2: int = Field(..., ge=0, le=4)
    family1: int = Field(..., ge=0, le=4)
    family2: int = Field(..., ge=0, le=4)
    family3: int = Field(..., ge=0, le=4)
    community1: int = Field(..., ge=0, le=4)
    community2: int = Field(..., ge=0, le=4)
    culture1: int = Field(..., ge=0, le=4)
    culture2: int = Field(..., ge=0, le=4)
    exploration1: int = Field(..., ge=0, le=4)
    exploration2: int = Field(..., ge=0, le=4)
    school1: int = Field(..., ge=0, le=4)

    @validator("media2", "family1", "family2", "family3", "community1", "community2", "culture1", "culture2", "exploration1", "exploration2", "school1")
    def ensure_int(cls, value: int) -> int:  # noqa: N805
        if not isinstance(value, int):
            raise TypeError("All answers must be integers")
        return value


class SectionScore(BaseModel):
    raw_score: int
    max_score: int
    percentage: float
    weight: float


class Interpretation(BaseModel):
    level: str
    description: str
    emoji: str
    range: str


class AnalysisResponse(BaseModel):
    timestamp: datetime
    overall_score: float
    interpretation: Interpretation
    section_scores: Dict[str, SectionScore]
    insights: List[str]
    disclaimer: str
    references: List[str]
