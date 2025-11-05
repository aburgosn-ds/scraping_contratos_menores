# =============================================================================
# processors/data_filter.py - Data filtering logic
# =============================================================================

import pandas as pd
from processors.text_analyzer import TextAnalyzer
import logging

from typing import List

class DataFilter:
    """Filter data based on text analysis."""
    
    def __init__(self, text_analyzer: TextAnalyzer):
        self.text_analyzer = text_analyzer
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def filter_by_topics(self, df: pd.DataFrame, description_column: str, accepted_topics: List[str]) -> pd.DataFrame:
        """Filter DataFrame based on topic analysis of description column."""
        if df.empty or description_column not in df.columns:
            self.logger.warning(f"DataFrame is empty or missing column: {description_column}")
            return pd.DataFrame()
        
        # Clean and prepare descriptions
        descriptions = df[description_column].fillna('').astype(str).tolist()
        
        # Analyze all descriptions
        self.logger.info(f"Analyzing {len(descriptions)} descriptions for topic relevance")
        topic_matches = self.text_analyzer.analyze_batch(descriptions, accepted_topics)
        
        # Filter DataFrame
        filtered_df = df[topic_matches].copy()
        
        self.logger.info(f"Filtered from {len(df)} to {len(filtered_df)} records")
        return filtered_df
