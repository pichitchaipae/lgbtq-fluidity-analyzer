import os
import openai
from functools import lru_cache
from typing import Any, Dict

class AIServiceError(Exception):
    """Custom exception for AI service errors."""
    pass

class AIInterpreter:
    """
    Service to get AI-powered interpretations of statistical results.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Please set the OPENAI_API_KEY environment variable.")
        self.client = openai.OpenAI(api_key=self.api_key)

    @lru_cache(maxsize=100)
    def get_interpretation(self, anova_results: Dict[str, Any], language: str = "th") -> str:
        """
        Gets a human-readable interpretation of ANOVA results from an AI model.
        Caches results to avoid redundant API calls.
        """
        sanitized_stats = self._sanitize_for_ai(anova_results)
        prompt = self._create_prompt(sanitized_stats, language)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a research psychologist specializing in LGBTQ+ studies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=400,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback for when the AI service fails
            raise AIServiceError(f"AI service request failed: {e}")

    def _sanitize_for_ai(self, anova_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts only aggregated, non-identifiable statistics to send to the AI.
        This is a critical privacy-preserving step.
        """
        table = anova_results.get("anova_table", {})

        def safe_get_stats(key):
            return {
                "F": round(table.get(key, {}).get("F", 0), 2),
                "p": round(table.get(key, {}).get("p_value", 1), 4),
                "eta_sq": round(table.get(key, {}).get("eta_sq", 0), 3)
            } if table.get(key) else None

        safe_payload = {
            "media_effect": safe_get_stats("C(media_group)"),
            "social_effect": safe_get_stats("C(social_group)"),
            "interaction_effect": safe_get_stats("C(media_group):C(social_group)"),
            "assumption_tests": anova_results.get("assumption_tests", {})
        }
        # Remove any None values
        return {k: v for k, v in safe_payload.items() if v is not None}

    def _create_prompt(self, sanitized_stats: Dict[str, Any], language: str) -> str:
        """Creates the detailed prompt for the AI model."""

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
        1.  Be supportive, non-judgmental, and use empowering language.
        2.  Clearly explain what each main effect (media, social) and the interaction effect means in practical terms.
        3.  Mention the statistical significance (e.g., "p < 0.05 indicates a significant effect").
        4.  Keep the explanation for each language concise (under 200 words).
        5.  {lang_instructions.get(language, lang_instructions['th'])}
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
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective model for chat
                messages=[
                    {"role": "system", "content": "You are a supportive educational assistant helping users understand their personal growth and identity survey results."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600,
            )
            
            if not response.choices or not response.choices[0].message.content:
                raise AIServiceError("AI response was empty or invalid.")
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise AIServiceError(f"OpenAI chatbot request failed: {str(e)}")