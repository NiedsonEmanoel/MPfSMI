import whisper
import os
from datetime import datetime

def formatar_timestamp(segundos):
    minutos, segundos = divmod(int(segundos), 60)
    horas, minutos = divmod(minutos, 60)
    return f"{horas:02}:{minutos:02}:{segundos:02}"

def transcrever_audio_paragrafos(caminho_audio, modelo="base", exportar=True):
    if not os.path.exists(caminho_audio):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_audio}")

    print(f"🔍 Carregando modelo Whisper: {modelo}...")
    model = whisper.load_model(modelo)

    print("📡 Iniciando transcrição com parágrafos...")
    result = model.transcribe(caminho_audio, verbose=False)

    paragrafos = []
    for segmento in result['segments']:
        inicio = formatar_timestamp(segmento['start'])
        fim = formatar_timestamp(segmento['end'])
        texto = segmento['text'].strip()
        paragrafos.append(f"[{inicio} - {fim}] {texto}")

    transcricao_formatada = "\n\n".join(paragrafos)

    print("\n✅ Transcrição finalizada com parágrafos!\n")
    print("-" * 60)
    print(transcricao_formatada)
    print("-" * 60)

    if exportar:
        salvar_transcricao_paragrafos(transcricao_formatada, caminho_audio)

    return transcricao_formatada


def salvar_transcricao_paragrafos(texto, caminho_audio):
    nome_base = os.path.splitext(os.path.basename(caminho_audio))[0]
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"transcricao_paragrafos_{nome_base}_{data}.txt"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"\n📁 Transcrição com parágrafos salva em: {nome_arquivo}")


# USO
if __name__ == "__main__":
    caminho = "seuarquivo.mp3"  # Altere aqui
    modelo = "small"            # Altere aqui se quiser outro
    try:
        transcrever_audio_paragrafos(caminho, modelo=modelo, exportar=True)
    except Exception as e:
        print(f"❌ Erro: {e}")