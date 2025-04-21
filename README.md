# 🎧 Audio to Resume

Transcreva áudios automaticamente com parágrafos organizados e timestamps usando o modelo Whisper.

---

## 🚀 Funcionalidades

- Transcrição automática de arquivos `.mp3`, `.wav`, `.m4a`, etc.  
- Divisão inteligente em parágrafos com timestamps.  
- Exportação em `.txt` para facilitar leitura e estudos.

---

## 📦 Requisitos

- Python 3.8+
- `torch`
- `openai-whisper`

---

## 🔧 Instalação

Clone o repositório e instale as dependências com:

```bash
pip install -r requirements.txt
```

---

## 🧠 Como usar

1. Coloque seu arquivo de áudio na raiz do projeto ou na pasta `examples/`.

2. Execute o script:

```bash
python transcriber.py
```

3. No código, você pode ajustar:

```python
caminho = "examples/seuarquivo.mp3"
modelo = "small"  # Opções: tiny, base, small, medium, large
```

---

## 📁 Saída

O arquivo `.txt` com a transcrição será salvo automaticamente com nome baseado no áudio original e data/hora da transcrição.

### 📌 Exemplo de saída:

```txt
[00:00 - 00:05] O paciente apresentava febre alta e calafrios.

[00:06 - 00:12] Durante o exame físico, notou-se hepatomegalia.
```

---

## 🧪 Modelos disponíveis

Você pode escolher entre os seguintes modelos Whisper (quanto maior, mais preciso e mais pesado):

- `tiny`
- `base`
- `small`
- `medium`
- `large`

---

## 📃 Licença

MIT License

---

Feito com ☕ e 🧠 por Niedson Emanoel, para me ajudar nas aulas de medicina.
