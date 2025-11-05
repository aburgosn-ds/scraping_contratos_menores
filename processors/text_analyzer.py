# =============================================================================
# processors/text_analyzer.py - Text analysis using Gemini
# =============================================================================

import google.generativeai as genai
from config.settings import GEMINI_CONFIG
from config.topics import TOPICS_CONFIG
import time
import logging

from typing import List

class TextAnalyzer:
    """Text analyzer using Google Gemini API."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        genai.configure(api_key=GEMINI_CONFIG['api_key'])
        self.model = genai.GenerativeModel(GEMINI_CONFIG['model'])
    
    def analyze_text_topic(self, text: str, accepted_topics: List[str]) -> bool:
        """Analyze if text relates to accepted topics."""
        try:
            prompt = TOPICS_CONFIG['analysis_prompt_template'].format(
                topics=', '.join(accepted_topics),
                text=text[:500]  # Limit text length for API
            )
            
            response = self.model.generate_content(prompt)
            result = response.text.strip().upper()
            
            return result == 'YES'
            
        except Exception as e:
            self.logger.error(f"Error analyzing text: {str(e)}")
            return False  # Conservative approach - exclude on error
    
    def analyze_batch(self, texts: List[str], accepted_topics: List[str]) -> List[bool]:
        """Analyze multiple texts with rate limiting."""
        results = []
        
        for i, text in enumerate(texts):
            result = self.analyze_text_topic(text, accepted_topics)
            results.append(result)
            
            # Add delay to respect API limits
            if i < len(texts) - 1:
                time.sleep(0.1)
        
        return results
