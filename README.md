# 🎧 Audio to Resume

Transcreva áudios automaticamente com organização em parágrafos e exportação com ou sem timestamps — usando o modelo Whisper da OpenAI.

Ideal para gerar **resumos**, **flashcards**, **perguntas**, ou **legendas sincronizadas** com base em áudios de aulas, entrevistas ou qualquer outro conteúdo falado.

---

## 🚀 Funcionalidades

- ✅ Transcrição automática de arquivos `.mp3`, `.wav`, `.m4a`, etc.
- ✅ Divisão inteligente em parágrafos.
- ✅ Exportação em `.txt` com e sem timestamps.
- ✅ Escolha do modelo Whisper (de `tiny` a `large`) via terminal.
- ✅ Suporte a CUDA (GPU) ou CPU, escolhido automaticamente.
- ✅ Pronto para integração com GPT para resumos, estudos e mais.

---

## 📦 Requisitos

- Python 3.8+
- [`torch`](https://pytorch.org/)
- [`openai-whisper`](https://github.com/openai/whisper)
- [`ntlk`](https://pypi.org/project/nltk/)

Instale com:

```bash
pip install torch openai-whisper nltk
```

Ou via `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🧠 Como usar

### 🎯 Modo rápido (com opções padrão)

```bash
python transcrever.py "caminho/para/audio.mp3"
```

Isso irá:
- Usar o modelo `base`
- Rodar em `cpu`
- Exportar `.txt` com e sem timestamps

---

### ⚙️ Modo avançado com flags

```bash
python transcrever.py "meuaudio.mp3" --modelo medium --sem-tempos
```

**Opções disponíveis:**

| Flag              | Descrição                                                  | Valor padrão |
|-------------------|------------------------------------------------------------|--------------|
| `--modelo`        | Modelo Whisper a ser usado: `tiny`, `base`, `small`, etc.  | `base`       |
| `--sem-tempos`    | Gera apenas a transcrição sem timestamps                   | *False*      |

---

## 🧪 Exemplos práticos

### 1. Transcrição simples com modelo pequeno:

```bash
python transcrever.py "aula_bioquimica.mp3" --modelo small
```

### 2. Transcrição só sem timestamps (ideal pra GPT):

```bash
python transcrever.py "palestra_neuro.m4a" --sem-tempos
```

---

## 📁 Saída

São gerados dois arquivos `.txt` na raiz do projeto:

- `com_tempos_nomeDoArquivo_DATA.txt`
- `sem_tempos_nomeDoArquivo_DATA.txt`

Exemplo de transcrição com timestamps:

```txt
[00:00 - 00:05] O paciente apresentava febre alta e calafrios.

[00:06 - 00:12] Durante o exame físico, notou-se hepatomegalia.
```

Exemplo sem timestamps:

```txt
O paciente apresentava febre alta e calafrios.

Durante o exame físico, notou-se hepatomegalia.
```

---

## 🧠 Dica para uso com ChatGPT

Se você quiser pedir resumos, flashcards ou gerar questões a partir da transcrição, use a versão **sem timestamps** para otimizar espaço e compreensão do conteúdo.

---

## 🧪 Modelos Whisper disponíveis

| Modelo   | Tamanho | Qualidade | Performance |
|----------|---------|-----------|-------------|
| `tiny`   | Leve    | Baixa     | Muito rápido |
| `base`   | Médio   | OK        | Rápido       |
| `small`  | Bom     | Boa       | Ok           |
| `medium` | Grande  | Muito boa | Mais lento   |
| `large`  | Enorme  | Excelente | Lento (sem GPU) |

---

## 📃 Licença

MIT License

---

Feito com ☕ e 🧠 por **Niedson Emanoel**, para me ajudar nas aulas de medicina — e agora pode ajudar você também!
