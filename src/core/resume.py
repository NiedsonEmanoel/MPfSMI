# MPfSMl - Medical Practice for Students on Machine Learning
# Niedson Emanoel, 21/04/2025.
# REFACTORY MADE 03/08/2025

import logging
from google import genai
from google.genai import types
from typing import Optional
from .utilities import load_file_content, build_config
from .searchImage import preparar_markdown_para_busca

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_resume(
    transcricao: str,
    key_path: Optional[str] = "../../gemini.key",
    prompt_path: Optional[str] = "../Prompts/Resumo.txt",
    model_name: str = "gemini-2.5-pro"
) -> str:
    """
    Gera um resumo em Markdown a partir de uma transcrição, usando Gemini API.
    """
    try:
        # Carregar chave e prompt
        api_key = load_file_content(key_path, "chave da API Gemini")
        prompt_text = load_file_content(prompt_path, "prompt do resumo")

        # Inicializar cliente Gemini
        client = genai.Client(api_key=api_key)

        # Preparar entrada
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=transcricao)],
            )
        ]

        config = build_config(prompt_text)

        # Gerar conteúdo
        logger.info("Iniciando geração do resumo com Gemini...")
        markdown_chunks = []
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config,
        ):
            markdown_chunks.append(chunk.text)

        logger.info("Resumo gerado com sucesso.")
        Resumen = ''.join(markdown_chunks)
        # Preparar o Markdown para busca de imagens
        Resumen = preparar_markdown_para_busca(Resumen)
        return Resumen
    
    except Exception as e:
        logger.exception("Erro ao gerar o resumo.")
        raise RuntimeError(f"Erro ao gerar o resumo: {e}")
