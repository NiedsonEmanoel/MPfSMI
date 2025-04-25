#MPfSMl - Medical pratice for Students on Machine learn 
#Niedson Emanoel, 21/04/2025.

import whisper
import argparse
import os
from datetime import datetime
import torch
import nltk
from nltk.corpus import stopwords
import string
import requests
import markdown
from weasyprint import HTML
import shutil
from google import genai
import json
import genanki
import random

# Lê a chave da API do arquivo gemini.key
with open("gemini.key", "r") as file:
    API_KEY = file.read().strip()

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

notion_style = """
<style>
  body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      max-width: 800px;
      margin: 40px auto;
      padding: 20px;
      line-height: 1.6;
      font-size: 16px;
      color: #333;
      background: #fff;
  }

  h1, h2, h3 {
      border-bottom: 1px solid #eaeaea;
      padding-bottom: 0.3em;
      margin-top: 1.4em;
  }

  code {
      background-color: #f6f8fa;
      padding: 2px 4px;
      border-radius: 3px;
      font-size: 90%;
      font-family: 'Courier New', Courier, monospace;
  }

  pre code {
      background-color: #f6f8fa;
      display: block;
      padding: 1em;
      overflow-x: auto;
  }

  blockquote {
      border-left: 4px solid #dfe2e5;
      padding: 0 1em;
      color: #6a737d;
  }

  table {
      border-collapse: collapse;
      width: 100%;
  }

  th, td {
      border: 1px solid #dfe2e5;
      padding: 6px 13px;
  }

  th {
      background-color: #f6f8fa;
  }

  @page {
      margin: 20mm;
  }
</style>
"""

headers = {
    "Content-Type": "application/json"
}

def argumentos_cli():
    parser = argparse.ArgumentParser(description="Transcrição e resumo de aulas com Whisper + Gemini")

    parser.add_argument('--audio', type=str, help='Caminho para o arquivo de áudio a ser processado')
    parser.add_argument('--modelo', type=str, default='base', help='Modelo do Whisper a ser usado (base, small, medium, large, etc.)')

    return parser.parse_args()

def gerar_pdf_markdown(markdown_text, pasta_destino, nome_pdf):
    html_content = markdown.markdown(markdown_text, extensions=["extra", "tables", "fenced_code"])
    full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{notion_style}</head><body>{html_content}</body></html>"
    caminho_pdf = os.path.join(pasta_destino, nome_pdf)
    HTML(string=full_html).write_pdf(caminho_pdf)
    print(f"✅ PDF gerado com sucesso: {caminho_pdf}")

def gerar_guia_estudos_markdown(transcricao: str) -> tuple[str, str]:
    prompt_estudo = f"""
A partir do conteúdo abaixo (resumo), crie uma guia de estudos personalizada em formato Markdown, com foco em aprendizado acadêmico e médico.

A resposta será convertida em PDF, então:

- Use formatação Markdown limpa
- Use títulos, listas e divisões visuais claras
- Não inclua elementos interativos ou links clicáveis

Contexto essencial:

Este resumo foi gerado a partir de um sistema automatizado que converte áudios de estudo em texto. A partir dele, serão produzidos:

- Questões objetivas e clínicas, classificadas por dificuldade
- Flashcards com os principais pontos e termos

Por isso, a guia de estudos deve:

- Indicar os conhecimentos prévios essenciais para compreender o tema
- Apresentar um checklist organizado com o que estudar primeiro
- Explicar como e quando utilizar as questões e flashcards gerados
- Evitar sugestões genéricas como "ensinar a alguém" ou "fazer resumos próprios"

A estrutura da resposta deve ser:

# Guia de Estudos: [Tema do Resumo]

## Visão Geral
Descreva em poucas linhas o tema central e sua relevância médica.

## Pré-requisitos
Liste tópicos que o estudante deve dominar antes de aprofundar o conteúdo. Ex: anatomia relacionada, princípios básicos, etc.

## Checklist de Estudo
Organize os principais pontos do conteúdo em forma de lista ordenada. Cada item deve representar uma etapa de estudo.

## Aplicação Direta
Oriente o estudante a:

- Usar as questões geradas para treinar sua compreensão e identificar lacunas
- Utilizar os flashcards para revisão contínua e memorização
- Revisar frequentemente os erros nas questões para reforçar áreas frágeis

Não inclua sugestões genéricas como ensinar o conteúdo para outra pessoa.

## Plano de Estudo Sugerido
Organize um cronograma de revisão dividido por dias (ex: 3, 7 ou 14 dias), integrando o uso das questões e dos flashcards gerados com o resumo.

Resumo para base do estudo:
{transcricao}
"""

    with open("gemini.key", "r") as file:
        API_KEY = file.read().strip()

    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}

    data = {"contents": [{"parts": [{"text": prompt_estudo}]}]}

    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        markdown_raw = result['candidates'][0]['content']['parts'][0]['text']
        
        markdown_clean = markdown_raw.strip().split("\n", 1)[-1].strip()  # Clean and trim the result
        
        titulo = next((line.strip("# ").strip() for line in markdown_clean.split("\n") if line.startswith("# ")), "Guia")
        return f"{titulo}.pdf", markdown_clean
    else:
        raise Exception(f"Erro na requisição: {response.status_code}\n{response.text}")

def gerar_resumo_markdown(transcricao: str) -> tuple[str, str]:
    prompt = f"""
Sem fornecer nenhum tipo de feedback, comentário ou explicação adicional, gere um resumo completo e didático da transcrição da aula que vou enviar a seguir. O objetivo é facilitar a compreensão de um aluno de medicina, então complemente com informações relevantes sempre que considerar útil para a assimilação do conteúdo.

O resumo deve ser entregue em Markdown puro, como se fosse um código-fonte, com títulos estilizados com emojis, no estilo visual do Notion.

Apenas retorne o conteúdo em Markdown, sem nenhuma outra resposta textual.

Transcrição da aula:
{transcricao}
"""

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        markdown_raw = result['candidates'][0]['content']['parts'][0]['text']

        if markdown_raw.startswith("```markdown") and markdown_raw.endswith("```"):
            markdown_clean = "\n".join(markdown_raw.strip().split("\n")[1:-1])
        else:
            markdown_clean = markdown_raw

        titulo = ""
        for line in markdown_clean.split("\n"):
            if line.strip().startswith("# "):
                titulo = line.strip("# ").strip()
                break

        titulo = titulo + '.pdf'
        return titulo, markdown_clean
    else:
        raise Exception(f"Erro na requisição: {response.status_code}\n{response.text}")

def escolher_dispositivo():
    return "cuda" if torch.cuda.is_available() else "cpu"

def formatar_timestamp(segundos):
    h, m = divmod(int(segundos), 3600)
    m, s = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}"

def remover_stopwords(texto):
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

def transcrever_audio(caminho_audio, modelo="base", exportar=True, dispositivo="cpu"):
    if not os.path.exists(caminho_audio):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_audio}")

    print(f"🔍 Carregando modelo Whisper '{modelo}' no dispositivo {dispositivo.upper()}...")
    model = whisper.load_model(modelo).to(dispositivo)

    print("📡 Transcrevendo áudio...")
    resultado = model.transcribe(caminho_audio, verbose=False)

    com_tempos = []
    sem_tempos = []

    for s in resultado['segments']:
        texto = s['text'].strip()
        com_tempos.append(f"[{formatar_timestamp(s['start'])} - {formatar_timestamp(s['end'])}] {texto}")
        sem_tempos.append(texto)

    texto_com_tempos = "\n\n".join(com_tempos)
    texto_sem_tempos = " ".join(sem_tempos)
    texto_sem_tempos = remover_stopwords(texto_sem_tempos)

    print("\n✅ Transcrição finalizada!\n")
    if exportar:
        salvar_transcricoes(texto_com_tempos, texto_sem_tempos, caminho_audio)

    return texto_com_tempos, texto_sem_tempos

def salvar_transcricoes(com_tempos, sem_tempos, caminho_audio):
    base = os.path.splitext(os.path.basename(caminho_audio))[0]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    arquivos = {
        f"com_tempos_{base}_{timestamp}.txt": com_tempos,
        f"sem_tempos_{base}_{timestamp}.txt": sem_tempos
    }

    for nome, conteudo in arquivos.items():
        with open(nome, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"📁 Arquivo salvo: {nome}")

def mover_arquivos_processados(pasta_destino, base_nome):
    extensoes = (".mp3", ".wav", ".m4a", ".txt", '.apkg')
    for arquivo in os.listdir("."):
        if base_nome in arquivo and arquivo.endswith(extensoes):
            origem = os.path.join(".", arquivo)
            destino = os.path.join(pasta_destino, arquivo)
            shutil.move(origem, destino)
            print(f"📦 Arquivo movido: {arquivo}")

def escolher_arquivo_audio(diretorio):
    arquivos_audio = [f for f in os.listdir(diretorio) if f.lower().endswith(('.mp3', '.wav', '.m4a'))]

    if len(arquivos_audio) == 0:
        print("❌ Nenhum arquivo de áudio encontrado na raiz.")
        return None

    if len(arquivos_audio) == 1:
        return arquivos_audio[0]

    print("🔊 Múltiplos arquivos de áudio encontrados. Escolha um para processar via flag --audio.")
    print('Ver documentação.')
    return (2/0)/0

def gerar_questoes_markdown(texto_base):
    prompt = f"""
    A partir do conteúdo abaixo, crie 10 questões de cada nível de dificuldade (fácil, médio, difícil), com foco em reforço de compreensão médica e acadêmica. Siga as regras:

    - Crie 10 questões fáceis, 10 médias e 10 difíceis.
    - Não agrupe as questões em fáceis, médias ou dificeis, o aluno só deve saber ao ver o gabarito.
    - Faça da questão 01 até a 30, sem agrupar por dificuldade.
    - As respostas das questões devem estar APENAS excluivamente na área de gabaritos.
    - As questões devem ser formuladas em formatos variados:
      - Questões objetivas (com alternativas)
      - Questões de resposta curta
      - Questões de verdadeiro ou falso
      - Casos clínicos

    - As alternativas, ou as respostas curtas, devem ser realistas e educativas, com a resposta correta claramente identificada.
    - As alternativas devem ser equilibradas em dificuldade, sem nenhuma óbvia ou excessivamente fácil.
    - Cada questão deve ser seguida de justificativa detalhada explicando o raciocínio por trás da resposta correta.
    - Não forneça explicações adicionais além das instruções acima.

    A saída deve estar no formato Markdown, com as questões bem organizadas e agradáveis para visualização e impressão. Evite usar links e mantenha a formatação simples, para que as questões sejam facilmente legíveis e prontas para serem impressas. As alternativas devem ser listadas de forma clara, e cada justificativa deve vir logo após a questão correspondente.

    Para as questões de resposta curta, inclua um espaço de linhas (sublinhado) do tamanho necessário para a resposta, usando a seguinte formatação:
    ________________________

    Saída: Responda no formato Markdown com as seguintes informações:

    ### Questões:
    
    1.  **Pergunta:** (enunciado da questão)  
       - Alternativas:
         - A) Alternativa 1
         - B) Alternativa 2
         - C) Alternativa 3
         - D) Alternativa 4
         - E) Alternativa 5

    2.  **Pergunta:** (enunciado da questão)  
       - Alternativas:
         - A) Verdadeiro
         - B) Falso (justificar aqui:______________________________)

    3. **Pergunta:** (enunciado da questão)  
       **Resposta:**  
       _____________________________________________________________  

    Repita as 30 questões, seguindo o mesmo formato

    ### Gabarito:
    1. **Resposta:** A  
       **Justificativa:** Explicação detalhada do porquê a alternativa A é a correta.
       **Nível: fácil/médio/difícil**  

    2. **Resposta:** B  
       **Justificativa:** Explicação detalhada do porquê a alternativa B é a correta.
       **Nível: fácil/médio/difícil**  

    3. **Resposta:** Falso  
       **Justificativa:** Explicação detalhada do que tornou a questão falsa ou verdadeira.
       **Nível: fácil/médio/difícil**  

    (Repita para todas as questões)

    ### Texto base:
    {texto_base}
    """
        # Lê a chave da API do arquivo gemini.key
    with open("gemini.key", "r") as file:
        API_KEY = file.read().strip()

    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}

    data = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        markdown_raw = result['candidates'][0]['content']['parts'][0]['text']
        
        markdown_clean = markdown_raw.strip().split("\n", 1)[-1].strip()  # Clean and trim the result
        
        titulo = 'questoes'
        return f"{titulo}.pdf", markdown_clean
    else:
        raise Exception(f"Erro na requisição: {response.status_code}\n{response.text}")

def gerarFlashcards(resumo):
    client = genai.Client(
        api_key=API_KEY
    )

    prompt = f"""

    A partir do conteúdo abaixo (resumo da transcrição), crie flashcards no formato JSON, com foco em aprendizado acadêmico e médico.

    A resposta será convertida em .apkg, então:

    - Use formatação JSON limpa, apenas o json sem nenhuma outra explicação
    - Cada flashcard deve ser composto por uma pergunta e sua resposta
    - Inclua as informações médicas essenciais, de forma objetiva e concisa

    Contexto essencial:

    Este conteúdo será usado para revisões rápidas e eficazes, com foco em memorização ativa para estudantes de medicina. Para isso, os flashcards devem:

    - Apresentar perguntas clínicas relevantes baseadas no conteúdo
    - Utilizar a estrutura "pergunta e resposta" de forma clara e objetiva
    - Evitar usar questões muito genéricas ou vagas

    Responda apenas com o JSON. Não adicione explicações extras.

    A estrutura da resposta deve ser:

    **Pergunta:** [Texto da pergunta]
    **Resposta:** [Texto da resposta]

    Resumo para base dos flashcards:
        {resumo}
    """

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    # Remove a primeira e a última linha da resposta
    preJson = '\n'.join(response.text.splitlines()[1:-1])

    # Converte string para JSON
    flashcards = json.loads(preJson)

    return(flashcards)

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

# 🧪 Execução direta
if __name__ == "__main__":
    #args = argumentos_cli()
    diretorio = "."  
    #arquivo_audio = args.audio if args.audio else escolher_arquivo_audio(diretorio)
    arquivo_audio = escolher_arquivo_audio(diretorio)

    if arquivo_audio:
        caminho_audio = os.path.join(diretorio, arquivo_audio)
        #modelo = args.modelo
        modelo = 'medium'
        dispositivo = escolher_dispositivo()

        # Usa o nome do arquivo de áudio (sem extensão) para criar a pasta
        nome_arquivo_sem_ext = os.path.splitext(arquivo_audio)[0]
        pasta_destino = os.path.join("aulas_processadas", nome_arquivo_sem_ext)

        if os.path.exists(pasta_destino):
            print(f"⚠️ Esta aula já foi processada anteriormente: {pasta_destino}")
        else:
            os.makedirs(pasta_destino)
            try:
                withTime, noTime = transcrever_audio(caminho_audio, modelo=modelo, exportar=True, dispositivo=dispositivo)

                print("\n📝 Criando resumo")
                tituloMD, resumoMD = gerar_resumo_markdown(noTime)
                print("\n✅ Resumo pronto!")

                print("\n📝 Criando guia de estudos")
                tituloGuia, guiaEstudos = gerar_guia_estudos_markdown(resumoMD)
                print("\n✅ Guia de estudos pronto!")

                print("\n📝 Criando questões")
                tituloQuestoes, QuestoesMD = gerar_questoes_markdown(resumoMD)
                print("\n✅ Questoes prontas!")

                gerar_pdf_markdown(resumoMD, pasta_destino, "resumo.pdf")
                gerar_pdf_markdown(guiaEstudos, pasta_destino, "guia.pdf")
                gerar_pdf_markdown(QuestoesMD, pasta_destino, "questoes.pdf")

                # Mover os arquivos usados para a pasta destino
                mover_arquivos_processados(pasta_destino, nome_arquivo_sem_ext)

            except Exception as erro:
                print(f"❌ Erro: {erro}")
