from pydub import AudioSegment
import os
import re

# Caminho da pasta com os áudios
pasta = "audio"

# Lista todos os arquivos de áudio da pasta
arquivos = [f for f in os.listdir(pasta) if f.endswith((".mp3", ".wav", ".ogg", ".m4a"))]

# Função para extrair número final do nome do arquivo
def extrair_numero(nome):
    match = re.search(r'(\d+)(?=\.\w+$)', nome)
    return int(match.group(1)) if match else 0

# Ordena os arquivos pelo número final
arquivos.sort(key=extrair_numero)

# Inicializa o áudio final vazio
audio_final = AudioSegment.empty()

# Concatena os áudios
for arquivo in arquivos:
    caminho = os.path.join(pasta, arquivo)
    audio = AudioSegment.from_file(caminho)
    audio_final += audio

# Exporta o áudio final
audio_final.export(os.path.join(pasta, "audio_unido.mp3"), format="mp3")

print("Áudio unido com sucesso!")
