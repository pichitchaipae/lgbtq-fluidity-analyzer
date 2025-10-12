"""
API routes for AI chatbot functionality.
Provides conversational AI analysis of individual survey results.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import os

from ..services.gemini_interpreter import GeminiInterpreter, GeminiServiceError
from ..services.ai_interpreter import AIInterpreter, AIServiceError

router = APIRouter(prefix="/chatbot", tags=["chatbot"])
limiter = Limiter(key_func=get_remote_address)

class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    """Request for chatbot conversation."""
    survey_result: Dict[str, Any] = Field(..., description="User's survey analysis result")
    message: str = Field(..., description="User's question or message")
    conversation_history: List[ChatMessage] = Field(default=[], description="Previous conversation")
    language: str = Field(default="th", description="Language for response (th/en)")

class ChatResponse(BaseModel):
    """Response from chatbot."""
    message: str = Field(..., description="AI assistant's response")
    suggestions: List[str] = Field(default=[], description="Suggested follow-up questions")

def get_ai_interpreter():
    """Get configured AI interpreter (Gemini or OpenAI)."""
    ai_provider = os.getenv("AI_PROVIDER", "gemini").lower()
    
    if ai_provider == "gemini":
        try:
            return GeminiInterpreter()
        except ValueError:
            try:
                return AIInterpreter()
            except ValueError:
                return None
    elif ai_provider == "openai":
        try:
            return AIInterpreter()
        except ValueError:
            try:
                return GeminiInterpreter()
            except ValueError:
                return None
    else:
        return None

@router.post("", response_model=ChatResponse)
@limiter.limit("20/minute")
async def chat(
    request: Request,
    payload: ChatRequest,
    ai_interpreter = Depends(get_ai_interpreter),
) -> ChatResponse:
    """
    Chat with AI about survey results.
    Provides conversational analysis and answers questions.
    """
    if not ai_interpreter:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is not available. Please configure GEMINI_API_KEY or OPENAI_API_KEY."
        )
    
    try:
        # Calculate scores from raw survey data
        # Section mappings
        sections = {
            "Media": ["media1", "media2"],
            "Family": ["family1", "family2", "family3"],
            "Community": ["community1", "community2"],
            "Culture": ["culture1", "culture2"],
            "Exploration": ["exploration1", "exploration2"],
            "School": ["school1"]
        }
        
        # Calculate section scores
        section_scores = {}
        total_score = 0
        total_max = 0
        
        for section_name, questions in sections.items():
            section_sum = sum(payload.survey_result.get(q, 0) for q in questions)
            section_max = len(questions) * 5  # Each question max is 5
            percentage = (section_sum / section_max * 100) if section_max > 0 else 0
            section_scores[section_name] = {
                "raw": section_sum,
                "max": section_max,
                "percentage": percentage
            }
            total_score += section_sum
            total_max += section_max
        
        overall_score = (total_score / total_max * 100) if total_max > 0 else 0
        
        # Determine interpretation (neutral language)
        if overall_score >= 70:
            interpretation = "High engagement level with survey topics"
        elif overall_score >= 40:
            interpretation = "Moderate engagement level with survey topics"
        else:
            interpretation = "Initial engagement with survey topics"
        
        # Create context for the AI (pure statistical data only)
        context_parts = []
        
        # Add language instruction
        if payload.language == "th":
            context_parts.append("ให้คำตอบเป็นภาษาไทย")
        else:
            context_parts.append("Respond in English")
        
        context_parts.append(f"\nStatistical Data:")
        context_parts.append(f"Overall: {overall_score:.1f}%")
        context_parts.append(f"\nBreakdown:")
        
        for section, scores in section_scores.items():
            context_parts.append(f"{section}: {scores['percentage']:.1f}%")
        
        # Add conversation history
        if payload.conversation_history:
            context_parts.append("\nPrevious Conversation:")
            for msg in payload.conversation_history[-5:]:  # Last 5 messages
                role = "User" if msg.role == "user" else "Assistant"
                context_parts.append(f"{role}: {msg.content}")
        
        context = "\n".join(context_parts)
        
        # Ultra-minimal prompt to avoid safety filters
        system_prompt = """Statistical analyst. Interpret data objectively."""

        full_prompt = f"{system_prompt}\n{context}\n\nQ: {payload.message}\nA:"
        
        # Get AI response using chat method
        response_text = ai_interpreter.chat(full_prompt, payload.language)
        
        # Generate suggested questions based on the result
        suggestions = generate_suggestions(overall_score, payload.language)
        
        return ChatResponse(
            message=response_text,
            suggestions=suggestions
        )
        
    except (AIServiceError, GeminiServiceError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )

def generate_suggestions(overall_score: float, language: str) -> List[str]:
    """Generate contextual follow-up question suggestions (neutral language)."""
    if language == "th":
        if overall_score >= 70:
            return [
                "คะแนนของฉันบ่งบอกอะไร?",
                "ฉันควรทำอย่างไรต่อไป?",
                "มีข้อมูลเพิ่มเติมไหม?",
                "การวิเคราะห์นี้หมายความว่าอย่างไร?"
            ]
        elif overall_score >= 40:
            return [
                "ผลลัพธ์นี้หมายความว่าอย่างไร?",
                "ฉันควรให้ความสนใจกับส่วนไหน?",
                "มีคำแนะนำสำหรับฉันไหม?",
                "ฉันควรเริ่มจากตรงไหน?"
            ]
        else:
            return [
                "คะแนนต่ำหมายความว่าอย่างไร?",
                "ฉันควรศึกษาเพิ่มเติมตรงไหน?",
                "มีทรัพยากรที่แนะนำไหม?",
                "ฉันจะเข้าใจผลลัพธ์นี้มากขึ้นได้อย่างไร?"
            ]
    else:  # English
        if overall_score >= 70:
            return [
                "What does my score indicate?",
                "What should I focus on next?",
                "Can you explain the results further?",
                "How do I interpret these findings?"
            ]
        elif overall_score >= 40:
            return [
                "What do these results mean?",
                "Which categories should I pay attention to?",
                "Do you have recommendations for me?",
                "Where should I begin?"
            ]
        else:
            return [
                "What does a lower score indicate?",
                "Where should I focus my learning?",
                "Are there resources you recommend?",
                "How can I better understand these results?"
            ]
