"""Google Gemini AI interpreter service for statistical results."""
import os
import google.generativeai as genai
from functools import lru_cache
from typing import Any, Dict


class GeminiServiceError(Exception):
    """Custom exception for Gemini service errors."""
    pass


class GeminiInterpreter:
    """
    Service to get AI-powered interpretations of statistical results using Google Gemini.
    FREE FOREVER: 15 requests/minute, 1 million tokens/day.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Please set the GEMINI_API_KEY environment variable.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.5 Flash (stable, fast, free tier)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    @lru_cache(maxsize=100)
    def get_interpretation(self, anova_results_str: str, language: str = "th") -> str:
        """
        Gets a human-readable interpretation of ANOVA results from Gemini AI.
        Caches results to avoid redundant API calls.
        
        Args:
            anova_results_str: JSON string of ANOVA results (for caching)
            language: Language code ('th' or 'en')
        
        Returns:
            Bilingual interpretation string
        """
        # Convert string back to dict for processing
        import json
        anova_results = json.loads(anova_results_str)
        
        sanitized_stats = self._sanitize_for_ai(anova_results)
        prompt = self._create_prompt(sanitized_stats, language)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=400,
                )
            )
            return response.text.strip()
        except Exception as e:
            # Fallback for when the AI service fails
            raise GeminiServiceError(f"Gemini AI service request failed: {e}")
    
    def _sanitize_for_ai(self, anova_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts only aggregated, non-identifiable statistics to send to Gemini.
        This is a critical privacy-preserving step.
        
        Args:
            anova_results: Full ANOVA results dictionary
        
        Returns:
            Dictionary with only statistical summaries (F, p, eta²)
        """
        table = anova_results.get("anova_table", {})
        
        def safe_get_stats(key):
            """Safely extract statistics for a specific effect"""
            if not table.get(key):
                return None
            return {
                "F": round(table.get(key, {}).get("F", 0), 2),
                "p": round(table.get(key, {}).get("p_value", 1), 4),
                "eta_sq": round(table.get(key, {}).get("eta_sq", 0), 3)
            }
        
        safe_payload = {
            "media_effect": safe_get_stats("C(media_group)"),
            "social_effect": safe_get_stats("C(social_group)"),
            "interaction_effect": safe_get_stats("C(media_group):C(social_group)"),
            "assumption_tests": anova_results.get("assumption_tests", {})
        }
        
        # Remove any None values
        return {k: v for k, v in safe_payload.items() if v is not None}
    
    def _create_prompt(self, sanitized_stats: Dict[str, Any], language: str) -> str:
        """
        Creates the detailed prompt for Gemini AI.
        
        Args:
            sanitized_stats: Sanitized statistical summaries
            language: Target language ('th' or 'en')
        
        Returns:
            Formatted prompt string
        """
        lang_instructions = {
            "th": "Provide the output in Thai first, followed by an English translation. Format it as:\n[TH]: <Thai explanation>\n[EN]: <English explanation>",
            "en": "Provide the output in English first, followed by a Thai translation. Format it as:\n[EN]: <English explanation>\n[TH]: <Thai explanation>"
        }
        
        return f"""
Analyze the following Two-Way ANOVA results from a study on LGBTQ+ sexual fluidity.

Statistical Results:
{sanitized_stats}

Your Task:
Explain these results in a way that is easy for a general audience to understand.

Requirements:
1. Be supportive, non-judgmental, and use empowering language.
2. Clearly explain what each main effect (media, social) and the interaction effect means in practical terms.
3. Mention the statistical significance (e.g., "p < 0.05 indicates a significant effect").
4. Keep the explanation for each language concise (under 200 words).
5. {lang_instructions.get(language, lang_instructions['th'])}

Important Notes:
- This is a study about LGBTQ+ sexual fluidity and identity exploration
- Media exposure refers to LGBTQ+ representation in media
- Social acceptance refers to acceptance from family, friends, and community
- The interaction effect shows how media and social factors work together
"""

    def chat(self, prompt: str, language: str = "en") -> str:
        """
        Get a conversational AI response for chatbot interactions.
        
        Args:
            prompt: Full prompt including context and user message
            language: Language code ('th' or 'en')
        
        Returns:
            AI-generated response text
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,  # Balanced temperature for factual yet warm responses
                    max_output_tokens=2048,  # เพิ่มจาก 600 -> 2048 เพื่อหลีกเลี่ยง MAX_TOKENS (finish_reason=2)
                ),
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE",
                    },
                ]
            )
            
            # จัดการกรณีไม่มี candidates หรือ parts (ตาม GitHub issue #373)
            candidates = getattr(response, "candidates", []) or []
            if not candidates:
                raise GeminiServiceError("No candidates returned. The request may have been blocked.")
            
            candidate = candidates[0]
            finish_reason = getattr(candidate, "finish_reason", None)
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", []) if content else []
            
            # เช็กว่ามี parts หรือไม่ (หลีกเลี่ยง response.text ที่ใช้ไม่ได้)
            if not parts:
                safety_ratings = getattr(candidate, "safety_ratings", []) or []
                safety_info = [f"{r.category}: {r.probability}" for r in safety_ratings]
                raise GeminiServiceError(
                    f"No content parts returned. finish_reason={finish_reason}. "
                    f"Safety ratings: {', '.join(safety_info) if safety_info else 'None'}. "
                    f"Try increasing max_output_tokens or shortening the prompt."
                )
            
            # รวมข้อความจากทุก parts
            text = "".join([getattr(p, "text", "") for p in parts])
            
            if not text or not text.strip():
                raise GeminiServiceError(
                    f"Empty response from Gemini. finish_reason={finish_reason}"
                )
            
            return text.strip()
        except GeminiServiceError:
            raise
        except Exception as e:
            raise GeminiServiceError(f"Gemini AI chatbot request failed: {str(e)}")
