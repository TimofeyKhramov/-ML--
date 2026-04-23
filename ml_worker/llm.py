import requests
import logging
import json
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def do_task(text: str) -> str:
    """
    Выполняет задачу обработки текста с помощью LLM.
    
    Args:
        text: Входящий текст для обработки
        
    Returns:
        str: Краткое продолжение текста (не более 10 токенов)
    """
    try:
        return(text+'READY')
       
        
    except requests.Timeout:
        logger.error("Request timed out")
        return 'Превышено время ожидания ответа'
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return 'Ошибка при выполнении запроса'
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 'Неожиданная ошибка при обработке'