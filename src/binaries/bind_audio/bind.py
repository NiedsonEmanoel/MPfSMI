import os
import re
import glob
from tqdm import tqdm
from pydub import AudioSegment


def natural_sort(files):
    """Ordena arquivos de forma natural (1, 2, 10 em vez de 1, 10, 2)."""
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', os.path.basename(key))]
    return sorted(files, key=alphanum_key)


def check_ffmpeg(base_dir):
    """Valida se ffmpeg e ffprobe estão disponíveis."""
    ffmpeg_bin_dir = os.path.join(base_dir, "..", "ffmpeg", "bin")
    ffmpeg_path = os.path.join(ffmpeg_bin_dir, "ffmpeg.exe")
    ffprobe_path = os.path.join(ffmpeg_bin_dir, "ffprobe.exe")

    if not os.path.isfile(ffmpeg_path):
        raise FileNotFoundError(f"ffmpeg.exe não encontrado: {ffmpeg_path}")
    if not os.path.isfile(ffprobe_path):
        raise FileNotFoundError(f"ffprobe.exe não encontrado: {ffprobe_path}")

    os.environ["PATH"] += os.pathsep + ffmpeg_bin_dir


def combine_audios(folder, output_filename="combined.m4a"):
    """Une todos os áudios de uma pasta em um único arquivo .m4a (AAC)."""
    files = glob.glob(os.path.join(folder, "*.*"))
    files = natural_sort(files)

    if not files:
        raise FileNotFoundError(f"Nenhum arquivo de áudio encontrado em: {folder}")

    combined = AudioSegment.empty()

    for file_path in tqdm(files, desc="Unindo áudios"):
        try:
            audio = AudioSegment.from_file(file_path)
            combined += audio
        except Exception as e:
            print(f"⚠️ Erro ao processar {file_path}: {e}")

    output_path = os.path.join(folder, output_filename)

    try:
        combined.export(output_path, format="mp4", codec="aac")
        print(f"\n✅ Áudios unidos com sucesso em: {output_path}")
    except Exception as e:
        raise RuntimeError(f"Falha ao exportar o áudio final: {e}")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    check_ffmpeg(BASE_DIR)

    folder = "audio"
    combine_audios(folder)
