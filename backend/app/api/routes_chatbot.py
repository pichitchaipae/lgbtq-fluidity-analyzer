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
        # Build context from survey result
        overall_score = payload.survey_result.get("overall_score", 0)
        interpretation = payload.survey_result.get("interpretation", {})
        section_scores = payload.survey_result.get("section_scores", {})
        
        # Create rich context for the AI
        context_parts = []
        
        # Add language instruction
        lang_instruction = "Please respond in Thai (ภาษาไทย)." if payload.language == "th" else "Please respond in English."
        context_parts.append(lang_instruction)
        
        context_parts.append(f"\nUser's Survey Results:")
        context_parts.append(f"Overall Score: {overall_score}%")
        context_parts.append(f"Interpretation: {interpretation.get('description', 'N/A')}")
        context_parts.append(f"\nSection Scores:")
        
        for section, scores in section_scores.items():
            if isinstance(scores, dict):
                percentage = scores.get('percentage', 0)
                context_parts.append(f"- {section}: {percentage:.1f}%")
        
        # Add conversation history
        if payload.conversation_history:
            context_parts.append("\nPrevious Conversation:")
            for msg in payload.conversation_history[-5:]:  # Last 5 messages
                role = "User" if msg.role == "user" else "Assistant"
                context_parts.append(f"{role}: {msg.content}")
        
        context = "\n".join(context_parts)
        
        # Create the full prompt
        system_prompt = """You are a supportive, knowledgeable, and empathetic AI assistant specializing in LGBTQ+ identity, sexual fluidity, and self-exploration. Your role is to:

1. Help users understand their survey results
2. Answer questions about sexual fluidity and identity
3. Provide supportive, non-judgmental guidance
4. Explain scores and what they might mean
5. Suggest resources or perspectives
6. Be respectful of all identities and experiences

Guidelines:
- Be warm, supportive, and affirming
- Use inclusive language
- Acknowledge that identity is personal and fluid
- Don't make assumptions about the user's identity
- Provide educational insights when relevant
- Respect privacy and confidentiality
- Encourage self-discovery at their own pace"""

        full_prompt = f"{system_prompt}\n\n{context}\n\nUser's Question: {payload.message}\n\nYour Response:"
        
        # Get AI response
        response_text = ai_interpreter.get_interpretation(full_prompt, payload.language)
        
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
    """Generate contextual follow-up question suggestions."""
    if language == "th":
        if overall_score >= 70:
            return [
                "คะแนนของฉันหมายความว่าอย่างไร?",
                "ฉันควรทำอะไรต่อไปดี?",
                "มีทรัพยากรหรือชุมชนที่แนะนำไหม?"
            ]
        elif overall_score >= 40:
            return [
                "ฉันกำลังสำรวจตัวเองอยู่ใช่ไหม?",
                "การรู้สึกแบบนี้เป็นเรื่องปกติไหม?",
                "ฉันควรเริ่มต้นจากตรงไหน?"
            ]
        else:
            return [
                "คะแนนต่ำหมายความว่าอย่างไร?",
                "ฉันควรกังวลไหม?",
                "ฉันจะเรียนรู้เพิ่มเติมได้อย่างไร?"
            ]
    else:  # English
        if overall_score >= 70:
            return [
                "What does my score mean?",
                "What should I do next?",
                "Are there communities or resources you recommend?"
            ]
        elif overall_score >= 40:
            return [
                "Am I exploring my identity?",
                "Is it normal to feel this way?",
                "Where should I start?"
            ]
        else:
            return [
                "What does a low score mean?",
                "Should I be concerned?",
                "How can I learn more?"
            ]
