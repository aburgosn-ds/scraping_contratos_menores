# =============================================================================
# processors/text_analyzer.py - Text analysis using Gemini
# =============================================================================

from google import genai
# import google.generativeai as genai
from google.genai import types
from config.settings import GEMINI_CONFIG
from config.topics import TOPICS_CONFIG
import time
import logging
import json
import ast
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

from typing import List

class TextAnalyzer:
    """Text analyzer using Google Gemini API."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = genai.Client(api_key='AIzaSyCMdfgJpQaVuNzc2pZ_a62674QWHB8S9NU')
        self.model_config = types.GenerateContentConfig(
            system_instruction=TOPICS_CONFIG['analysis_prompt_'],
            response_mime_type=GEMINI_CONFIG['response_mime_type'],
        )
    
    def _get_input(self, df):
        input_ = {key: value for key, value in zip(df.codigo.tolist(), df.descripcion.tolist())}
        input_ = json.dumps(input_, ensure_ascii=False)
        return input_

    def analyze_text_topic(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze if text relates to accepted topics."""
        try:
            self.logger.info(f"Generating content...")
            response = self.client.models.generate_content(
                model=GEMINI_CONFIG['model'],
                config=self.model_config,
                contents=self._get_input(df)
            )
            self.logger.info(f"Classification Done")

            result_as_list = ast.literal_eval(response.text)
            result_as_df = pd.DataFrame({'codigo': list(result_as_list.keys()), 'util': list(result_as_list.values())})

            df['codigo'] = df['codigo'].astype(str)
            result_as_df['codigo'] = result_as_df['codigo'].astype(str)

            df_final = df.join(result_as_df.set_index('codigo'), on='codigo', how='left')
            df_final['util'] = df_final.util.astype('int')

            df_final['cotizacion_comienzo'] = pd.to_datetime(df_final.cotizacion_comienzo, dayfirst=True)
            df_final['cotizacion_fin'] = pd.to_datetime(df_final.cotizacion_fin, dayfirst=True)
            
            self.logger.info(f"Procesed Dataframe generated correctly")

            return df_final
            
        except Exception as e:
            self.logger.error(f"Error analyzing text: {str(e)}")
            return False  # Conservative approach - exclude on error
