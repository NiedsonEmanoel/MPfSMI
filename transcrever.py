import whisper
import os
from datetime import datetime
import torch
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import argparse

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
        nltk.download('punkt')

    stop_words = set(stopwords.words("portuguese"))
    palavras = word_tokenize(texto, language='portuguese')
    palavras_filtradas = [
        palavra for palavra in palavras
        if palavra.lower() not in stop_words and palavra not in string.punctuation
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


def parse_args():
    parser = argparse.ArgumentParser(description="Transcrição de áudio com Whisper.")
    parser.add_argument("arquivo", help="Caminho para o arquivo de áudio")
    parser.add_argument("--modelo", default="base", help="Modelo Whisper a ser usado (base, small, medium, large)")
    parser.add_argument("--sem-tempos", action="store_true", help="Exportar apenas transcrição sem timestamps")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    try:
        texto = transcrever_audio(
            caminho_audio=args.arquivo,
            modelo=args.modelo,
            dispositivo=escolher_dispositivo(),
            incluir_tempos=not args.sem_tempos
        )
        print("\n📝 Transcrição (parcial):")
        print(texto[:1000])  # imprime os primeiros 1000 caracteres
    except Exception as erro:
        print(f"❌ Erro: {erro}")
