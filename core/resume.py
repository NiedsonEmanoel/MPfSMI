import os
from google import genai
from google.genai import types


def generateResume(transcricao: str) -> str:
    key_path = os.path.join(os.path.dirname(__file__), "..", "gemini.key")
    key_path = os.path.abspath(key_path)  # Resolve caminho absoluto

    if not os.path.exists(key_path):
        raise FileNotFoundError("Arquivo 'gemini.key' não encontrado!")

    with open(key_path, "r") as file:
        API_KEY = file.read().strip()

    client = genai.Client(
        api_key=API_KEY,
    )

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=transcricao),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=tools,
        system_instruction=[
            types.Part.from_text(text="""Sem fornecer comentários, explicações ou qualquer texto adicional fora do solicitado, gere um resumo técnico, didático e completo da transcrição da aula abaixo.

O conteúdo deve ser integralmente fiel à transcrição, sem omissões de informações relevantes — mesmo que aparentem ser redundantes.
Sempre que necessário para garantir clareza, preencha lacunas conceituais com explicações embasadas e complementos técnicos adequados ao nível de um aluno de medicina.

Inclua, quando pertinente, contextos clínicos, fisiológicos, anatômicos ou embriológicos que favoreçam a assimilação do tema.

O resumo deve ser entregue exclusivamente em Markdown puro, formatado no estilo visual do Notion:

Use títulos com seções hierárquicas organizadas (com #, ##, ###).

Utilize listas, subtópicos, tabelas e destaques visuais sempre que for útil à didática.

Para conceitos que exigem suporte visual para pleno entendimento:

insira no local apropriado a marca (IMAGEM: descrição precisa do que deve ser pesquisado no Google Images), sem fornecer links ou imagens, apenas a descrição exata e sucinta do que deve ser procurado. Faça a adição de imagens apenas em locais extremamente importantes e imprescindíveis ao aprendizado, para evitar poluir o PDF.

Seja objetivo, técnico e pedagogicamente organizado.

Retorne apenas o conteúdo em Markdown, sem qualquer outro tipo de resposta.
"""),
        ],
    )

    # Acumula o markdown gerado
    markdown_chunks = []

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        markdown_chunks.append(chunk.text)

    return ''.join(markdown_chunks)

# Exemplo de uso:
if __name__ == "__main__":
    texto_transcricao = "INSIRA AQUI SUA TRANSCRIÇÃO"  # Substituir por entrada real
    markdown_resultado = generateResume(texto_transcricao)
    print(markdown_resultado)  # ou use como retorno para salvar em PDF, etc.
