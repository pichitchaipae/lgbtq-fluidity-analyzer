import os
import json
from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..schemas.analysis_v2 import AnalysisV2Request, AnalysisV2Response
from ..services.analyzer import LGBTQAnalyzer
from ..services.ai_interpreter import AIInterpreter, AIServiceError
from ..services.gemini_interpreter import GeminiInterpreter, GeminiServiceError

router = APIRouter(prefix="/v2/analysis", tags=["analysis_v2"])
limiter = Limiter(key_func=get_remote_address)

def get_analyzer() -> LGBTQAnalyzer:
    return LGBTQAnalyzer()

def get_ai_interpreter():
    """
    Returns AI interpreter based on AI_PROVIDER environment variable.
    Supports: 'gemini' (default, free forever) or 'openai'
    """
    ai_provider = os.getenv("AI_PROVIDER", "gemini").lower()
    
    if ai_provider == "gemini":
        try:
            return GeminiInterpreter()
        except ValueError:
            # Gemini key not set, try OpenAI as fallback
            try:
                return AIInterpreter()
            except ValueError:
                return None
    elif ai_provider == "openai":
        try:
            return AIInterpreter()
        except ValueError:
            # OpenAI key not set, try Gemini as fallback
            try:
                return GeminiInterpreter()
            except ValueError:
                return None
    else:
        # Unknown provider, return None
        return None

@router.post("", response_model=AnalysisV2Response)
@limiter.limit("10/minute")
async def analyze_dataset(
    request: Request, # Required for slowapi
    payload: AnalysisV2Request,
    analyzer: LGBTQAnalyzer = Depends(get_analyzer),
    ai_interpreter: AIInterpreter = Depends(get_ai_interpreter),
) -> AnalysisV2Response:
    """
    Performs a Two-Way ANOVA on a dataset and optionally provides AI-powered insights.
    """
    anova_results = analyzer.analyze_two_way_anova(payload.dataset)

    if "error" in anova_results:
        # Handle cases like small sample size gracefully
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=anova_results.get("message", "Invalid dataset for analysis."),
        )

    ai_interpretation = None
    privacy_notice = "AI interpretation not requested. All calculations performed locally."
    ai_provider = os.getenv("AI_PROVIDER", "gemini")

    if payload.ai_insights:
        if not ai_interpreter:
            # AI service is not configured on the server
            ai_interpretation = "AI service is not available. Please set GEMINI_API_KEY or OPENAI_API_KEY environment variable."
            privacy_notice = "AI service not configured. All calculations performed locally."
        else:
            try:
                # Convert anova_results to JSON string for caching
                anova_results_str = json.dumps(anova_results)
                ai_interpretation = ai_interpreter.get_interpretation(anova_results_str, payload.language)
                privacy_notice = f"AI insights generated using {ai_provider.upper()}. Only aggregated, non-identifiable statistical summaries were sent to the AI service for interpretation."
            except (AIServiceError, GeminiServiceError) as e:
                # Fallback if the AI service fails
                ai_interpretation = f"AI interpretation failed: {e}. Displaying statistical results only."
                privacy_notice = "An error occurred with the AI service. No data was sent."

    return AnalysisV2Response(
        anova_results=anova_results["anova_table"],
        ai_interpretation=ai_interpretation,
        visualizations=anova_results["visualizations"],
        privacy_notice=privacy_notice,
    )