# src/core/transcription_youtube.py
# 18/08/25 NIEDSON EMANOEL - BRANCH MAC

from youtube_transcript_api import YouTubeTranscriptApi
import re

def transcrever_youtube(url: str, languages=['pt', 'pt-BR', 'en']):
    """
    Retorna transcrição do YouTube se disponível.
    """
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("URL inválida. Forneça um link válido do YouTube.")
    
    video_id = match.group(1)
    api = YouTubeTranscriptApi()
    fetched = api.fetch(video_id, languages=languages)
    
    texto = " ".join([snippet.text for snippet in fetched])
    return texto
