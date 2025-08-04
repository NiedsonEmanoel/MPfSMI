import os
from google.genai import types
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_file_content(file_path: str, description: str = "arquivo") -> str:
    """
    Carrega o conteúdo de um arquivo e retorna como string.
    """
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{description.capitalize()} não encontrado: {file_path}")
    
    logger.info(f"Carregando {description} de: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def build_config(prompt: str) -> types.GenerateContentConfig:
    """
    Cria a configuração para o modelo Gemini com o prompt e ferramentas adicionais.
    """
    return types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=[types.Tool(googleSearch=types.GoogleSearch())],
        system_instruction=[types.Part.from_text(text=prompt)],
    )