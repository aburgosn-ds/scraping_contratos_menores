# =============================================================================
# processors/data_filter.py - Data filtering logic from database
# =============================================================================

import pandas as pd
from processors.text_analyzer import TextAnalyzer
import logging

from typing import List

class DataFilter:
    """Filter data based on database comparision."""
    def __init__(self, new_data: pd.DataFrame):
        self.new_data = new_data
        self.logger = logging.getLogger(self.__class__.__name__)


    def df_filter_old_data(self, current_ids: list) -> pd.DataFrame:
        '''Returns data not in database'''
        new_records = ~self.new_data['codigo'].isin(current_ids)
        
        self.logger.info(f"Data filtered:\n\t-> New Data:{len(self.new_data)}\n\t-> Old Data:{len(current_ids)}\n\t-> Final Data: {len(new_records)}")
        return self.new_data[new_records]