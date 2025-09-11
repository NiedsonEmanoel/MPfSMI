# 🎧 MPfSML - Medical Practice for Students on Machine Learning  

Um aplicativo em **Streamlit** que processa **áudios e vídeos de aulas médicas**, gerando automaticamente:  
- 📄 **Resumos em PDF**  
- ❓ **Listas de questões clínicas**  
- 🃏 **Flashcards para Anki**  

Tudo isso com **IA Gemini (Google)** e transcrição de áudio via **Whisper**.  

---

## ✅ Funcionalidades  

- 🎙️ **Transcrição de áudio** (`.mp3`, `.wav`, `.m4a`) com modelos Whisper (tiny → large).  
- 📺 **Transcrição de vídeos do YouTube** diretamente pela URL.  
- ✍️ **Resumo didático em Markdown** via **API Gemini**, exportado como PDF.  
- ❓ **Geração de questões clínicas** automáticas em PDF.  
- 🃏 **Flashcards em `.apkg` para Anki**, prontos para revisão.  
- 📦 **Download em ZIP** contendo todos os materiais gerados.  
- 🚀 **Interface amigável em Streamlit**, sem necessidade de usar terminal.  
![Tela do MPfSMl](https://raw.githubusercontent.com/NiedsonEmanoel/MPfSMI/refs/heads/main/img/home.png)
---

## 🧭 Visão Geral do Fluxo do MPfSMl

O diagrama abaixo resume de forma clara o funcionamento do MPfSMl — desde a entrada de áudio até a geração dos materiais de estudo automatizados:

![Fluxo do MPfSMl](https://raw.githubusercontent.com/NiedsonEmanoel/MPfSMI/refs/heads/main/MPfSML.png)

> O sistema foi pensado para transformar qualquer aula (inclusive aulas ruins) em aprendizado ativo, integrado e automatizado, com mínimo esforço do aluno.

---

## 🚀 Como Executar  

### 1. Clonar o repositório  

```bash
git clone https://github.com/SEU_USUARIO/MPfSML.git
cd MPfSML
```

### 2. Instalar dependências  

```bash
pip install -r requirements.txt
```

> Certifique-se de ter o **FFmpeg** instalado para o Whisper.  

### 3. Rodar o aplicativo  

```bash
streamlit run main.py
```

O app abrirá no navegador em:  
👉 [http://localhost:8501](http://localhost:8501)  

---

## 🔑 Configuração da API Gemini  

1. Crie uma chave em: [Google AI Studio](https://aistudio.google.com/app/apikey)  
2. No primeiro uso, insira sua chave na tela de login do app.  
3. A chave será salva na **sessão do Streamlit**.  

---

## 📁 Estrutura do Projeto  

```
📂 MPfSML/
├── main.py                  # Aplicativo principal (Streamlit)
├── 📂 src/core/              # Funções principais
│   ├── resume.py            # Geração de resumos (Gemini)
│   ├── questions.py         # Geração de questões (Gemini)
│   ├── flashcards.py        # Geração de flashcards Anki
│   ├── pdfExport.py         # Exportação para PDF
│   ├── transcription_whisper.py  # Transcrição de áudio
│   ├── transcription_youtube.py  # Transcrição de vídeos
│   └── utilities.py
├── requirements.txt
├── img/
│   ├── rephraise_logo.png
│   └── image_banner.png
```

---

## 🃏 Flashcards Anki  

Os flashcards são gerados automaticamente em formato `.apkg`.  
- Baseados no **conteúdo transcrito**.  
- Estruturados em **Pergunta/Resposta**.  
- Importáveis diretamente no **Anki**.  

---

## 🧪 Modelos Whisper  

| Modelo   | Qualidade     | Velocidade |
|----------|---------------|------------|
| `tiny`   | Baixa         | Muito rápida |
| `base`   | OK            | Rápida       |
| `small`  | Boa           | Moderada     |
| `medium` | Muito boa     | Mais lenta   |
| `large`  | Excelente     | Lenta        |

---

## 📌 Requisitos  

- Python 3.9+  
- [FFmpeg](https://ffmpeg.org/download.html)  
- 8GB RAM (recomendado)  
- Opcional: GPU CUDA para acelerar o Whisper  

---

## 👨‍💻 Autor  

Feito com ☕ e 🧠 por **Niedson Emanoel**  
> Para mim e para todos os estudantes de medicina que acreditam no poder da tecnologia para aprender melhor.  
