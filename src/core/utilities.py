# MPfSMl - Medical Practice for Students on Machine Learning
# Author: Niedson Emanoel - 03/04/2025
# REFACTORY MADE 04/08/2025
    # This file contains utility functions for loading file content, building configuration for the Gemini model, and selecting the device for execution and other tasks.
    # Este arquivo contém funções utilitárias para carregar o conteúdo de arquivos, construir a configuração para o modelo Gemini e selecionar o dispositivo para execução e entre outros.

import os
from google.genai import types
import torch
import nltk
from nltk.corpus import stopwords
import string
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

def formatar_timestamp(segundos):
    h, m = divmod(int(segundos), 3600)
    m, s = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}"

def build_config(prompt: str) -> types.GenerateContentConfig:
    """
    Cria a configuração para o modelo Gemini com o prompt e ferramentas adicionais.
    """
    return types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=[types.Tool(googleSearch=types.GoogleSearch())],
        system_instruction=[types.Part.from_text(text=prompt)],
    )

def escolher_dispositivo() -> str:
    """
    Seleciona o dispositivo para execução (GPU ou CPU).
    Retorna "cuda" se disponível, caso contrário "cpu".
    """
    return "cuda" if torch.cuda.is_available() else "cpu"

def remover_stopwords(texto: str) -> str:
    """Remove stopwords do texto em português.
    Args:
        texto (str): Texto de entrada.
    """
    try:
        stopwords.words('portuguese')
    except LookupError:
        nltk.download('stopwords')

    stop_words = set(stopwords.words("portuguese"))
    texto_sem_pontuacao = texto.translate(str.maketrans('', '', string.punctuation))
    palavras = texto_sem_pontuacao.split()

    palavras_filtradas = [
        palavra for palavra in palavras
        if palavra.lower() not in stop_words
    ]
    return " ".join(palavras_filtradas)