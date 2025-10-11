"""HTTP endpoints for the analysis API."""
from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas.analysis import AnalysisRequest, AnalysisResponse
from ..services.analyzer import LGBTQAnalyzer

router = APIRouter(prefix="/analysis", tags=["analysis"])


def get_analyzer() -> LGBTQAnalyzer:
    return LGBTQAnalyzer()


@router.post("", response_model=AnalysisResponse)
async def analyze_answers(payload: AnalysisRequest, analyzer: LGBTQAnalyzer = Depends(get_analyzer)) -> AnalysisResponse:
    try:
        result = analyzer.analyze(payload.dict())
    except ValueError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return AnalysisResponse.model_validate(asdict(result))
