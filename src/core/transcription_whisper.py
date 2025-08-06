# MPfSMl - Medical Practice for Students on Machine Learning
# Niedson Emanoel, 21/04/2025.
# REFACTORY MADE 03/08/2025

import os
import whisper
from datetime import datetime
from utilities import remover_stopwords, escolher_dispositivo
sigla = "pt"  # Defina a sigla do idioma desejado, por exemplo, "pt" para português

# Caminho do diretório atual (src/core)
caminho_atual = os.path.dirname(os.path.abspath(__file__))
# Caminho absoluto para src/binaries/ffmpeg/bin
caminho_ffmpeg = os.path.abspath(os.path.join(caminho_atual, "..", "binaries", "ffmpeg", "bin"))
# Adiciona ao PATH
os.environ["PATH"] = caminho_ffmpeg + os.pathsep + os.environ["PATH"]

def formatar_timestamp(segundos):
    h, m = divmod(int(segundos), 3600)
    m, s = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}"

def salvar_transcricoes(com_tempos, sem_tempos, caminho_audio):
    base = os.path.splitext(os.path.basename(caminho_audio))[0]
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    arquivos = {
        f"com_tempos_{base}.txt": com_tempos,
        f"sem_tempos_{base}.txt": sem_tempos
    }

    for nome, conteudo in arquivos.items():
        with open(nome, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"📁 Arquivo salvo: {nome}")

def transcrever_audio(caminho_audio, modelo="base", exportar=True):
    dispositivo = escolher_dispositivo()
    if not os.path.exists(caminho_audio):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_audio}")

    print(f"🔍 Carregando modelo Whisper '{modelo}' no dispositivo {dispositivo.upper()}...")
    model = whisper.load_model(modelo).to(dispositivo)

    print("📡 Transcrevendo áudio...")
    resultado = model.transcribe(caminho_audio, verbose=False, language=sigla)

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

withtime, noTime = transcrever_audio('audioteste.mp3', modelo='base', exportar=True)