# MPfSMl - Medical Practice for Students on Machine Learning
# Niedson Emanoel, 21/04/2025.
# REFACTORY MADE 03/08/2025

import logging
from google import genai
from google.genai import types
from typing import Optional
from utilities import load_file_content, build_config
import json
import re
import random
import genanki

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extrair_json(texto):
    try:
        # Tenta extrair um bloco JSON entre colchetes
        match = re.search(r"\[\s*{.*}\s*\]", texto, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("JSON não encontrado no texto.")
    except Exception as e:
        raise RuntimeError(f"Falha ao extrair JSON: {e}")
    
def criar_baralho(flashcards, nome_baralho):
    # IDs únicos (você pode gerar novos com random.randint se quiser)
    modelo_id = 1607392319
    baralho_id = random.randint(1 << 28, (1 << 30) - 1)

    # Modelo do Anki
    modelo = genanki.Model(
        model_id=modelo_id,
        name='MPfSMl',
        fields=[
            {'name': 'Pergunta'},
            {'name': 'Resposta'},
        ],
        templates=[
            {
                'name': 'Cartão MPfSMl',
                'qfmt': '{{Pergunta}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Resposta}}',
            },
        ]
    )

    nameBaralho = 'MPfSMl::'+nome_baralho

    # Baralho
    baralho = genanki.Deck(
        deck_id=baralho_id,
        name=nameBaralho
    )

    # Adiciona flashcards
    for card in flashcards:
        nota = genanki.Note(
            model=modelo,
            fields=[card['Pergunta'], card['Resposta']]
        )
        baralho.add_note(nota)

    # Salva na raiz
    nome_arquivo = f'{nome_baralho}.apkg'
    genanki.Package(baralho).write_to_file(nome_arquivo)
    print(f'Baralho "{nome_arquivo}" criado com sucesso na raiz!')

def gerarFlashcards(
    resumo: str,
    key_path: Optional[str] = "../../gemini.key",
    prompt_path: Optional[str] = "../Prompts/GerarFlashCards.txt",
    model_name: str = "gemini-2.5-pro"
):
    try:
        # Modelo que você quer usar
        api_key = load_file_content(key_path, "chave da API Gemini")
        prompt_text = load_file_content(prompt_path, "prompt dos flashcards")

        client = genai.Client(api_key=api_key)

        # Preparar entrada
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=resumo)],
            )
        ]

        config = build_config(prompt_text)

        # Geração do conteúdo
        logger.info("Iniciando geração dos Flashcards com Gemini...")
        #response = client.generate_content(model=model_name,contents=contents,config=config)
        response_chunks = []
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config,
        ):
            response_chunks.append(chunk.text)
        response = ''.join(response_chunks)
        logger.info("Flashcards gerados com sucesso.")
        response = response.strip()
        response = extrair_json(response)
        logger.info("Flashcards gerados com sucesso.")
        return(response)
    except Exception as e:
        logger.exception("Erro ao gerar o Flashcard.")
        raise RuntimeError(f"Erro ao gerar o Flashcard: {e}")



flash=gerarFlashcards(resumo="""
A insuficiência cardíaca é uma síndrome clínica complexa caracterizada pela incapacidade do coração de bombear sangue adequadamente para suprir as necessidades metabólicas do organismo. Pode ser classificada como sistólica, quando há disfunção na contração ventricular, ou diastólica, quando há comprometimento no relaxamento e enchimento do ventrículo.

Os principais sintomas incluem dispneia, fadiga e edema periférico. A ausculta pulmonar pode revelar estertores e a avaliação física frequentemente mostra turgência jugular e hepatomegalia. A classificação funcional de NYHA ajuda a avaliar a gravidade.

Do ponto de vista fisiopatológico, a insuficiência cardíaca ativa sistemas compensatórios, como o sistema renina-angiotensina-aldosterona e o sistema nervoso simpático, que, apesar de inicialmente benéficos, contribuem para o agravamento da doença a longo prazo.

O tratamento envolve mudanças no estilo de vida, uso de IECA, betabloqueadores, diuréticos e, em casos avançados, dispositivos como CDI ou transplante cardíaco. A monitorização constante e o ajuste da terapêutica são fundamentais para reduzir hospitalizações e melhorar a qualidade de vida do paciente.

""")
