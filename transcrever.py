import whisper
import os
from datetime import datetime
import torch
import nltk
from nltk.corpus import stopwords
import string
import requests
import markdown
from weasyprint import HTML
import re

# Lê a chave da API do arquivo gemini.key
with open("gemini.key", "r") as file:
    API_KEY = file.read().strip()

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

notion_style = """
<style>
  body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Segoe UI Emoji", "Apple Color Emoji";
      max-width: 800px;
      margin: 10px auto; /* Margens menores */
      padding: 10px;  /* Ajuste no padding */
      line-height: 1.6;
      font-size: 16px;
      color: #2e2e2e;
      background: #ffffff;
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
        font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
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
    /* Definir margens menores para as páginas */
    @page {
        margin: 10mm;  /* Definindo margens menores para a página */
    }
</style>
"""

def gerar_pdf_markdown(markdown_text):
    nome_pdf="resumo.pdf"
    # Converter o Markdown para HTML
    html_content = markdown.markdown(markdown_text, extensions=["extra", "tables", "fenced_code"])

    # Combinar o estilo com o conteúdo HTML
    full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{notion_style}</head><body>{html_content}</body></html>"

    # Gerar o PDF com margens menores
    HTML(string=full_html).write_pdf(nome_pdf)

    print(f"✅ PDF gerado com sucesso: {nome_pdf}")

headers = {
    "Content-Type": "application/json"
}

def gerar_resumo_markdown(transcricao: str) -> tuple[str, str]:
    """
    Envia uma transcrição de aula para a API Gemini e retorna:
    - O resumo em Markdown (sem as marcações ```markdown)
    - O título (primeira linha que começa com '# ')
    """
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

        # Remove o bloco de código Markdown
        if markdown_raw.startswith("```markdown") and markdown_raw.endswith("```"):
            markdown_clean = "\n".join(markdown_raw.strip().split("\n")[1:-1])
        else:
            markdown_clean = markdown_raw

        # Extrai o primeiro título (linha que começa com '# ')
        titulo = ""
        for line in markdown_clean.split("\n"):
            if line.strip().startswith("# "):
                titulo = line.strip("# ").strip()
                break
        
        titulo = titulo+'.pdf'
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
    # Remove pontuação do texto antes de dividir
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

# 🧪 Execução direta
if __name__ == "__main__":
    caminho = r"C:\Users\nieds\OneDrive\Documents\GitHub\audioToResume\aulalindon.mp3"
    modelo = "medium"
    dispositivo = escolher_dispositivo()

    try:
        withTime, noTime = transcrever_audio(caminho, modelo=modelo, exportar=True, dispositivo=dispositivo)
        tituloMD, resumoMD = gerar_resumo_markdown(noTime)
        gerar_pdf_markdown(resumoMD) 
    except Exception as erro:
        print(f"❌ Erro: {erro}")


