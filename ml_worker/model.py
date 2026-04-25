import joblib
import numpy as np
import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class ModelService:
    """Сервис для загрузки и использования модели sklearn"""
    
    def __init__(self, model_path: str = None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "model_kNN.pkl")
        self.model_path = model_path
        self._model = None
    
    def _load_model(self):
        """Загружает модель из файла"""
        if self._model is None:
            try:
                self._model = joblib.load(self.model_path)
                logger.info(f"Model loaded from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise
    
    def predict(self, features: dict):
       
        self._load_model()
        
        df = pd.DataFrame([features])
        df.columns = ['Hb_tot', 'SpO2', 'Scat','intense_at_565', 'intense_at_520', 'lambdas']
       
        prediction = self._model.predict(df)
        return prediction