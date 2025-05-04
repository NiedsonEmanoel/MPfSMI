# 🎧 MPfSMl - Medical Practice for Students on Machine Learning 

Este projeto permite transcrever áudios (como aulas, reuniões, entrevistas) usando o modelo [`whisper`](https://github.com/openai/whisper), gerar um resumo didático em Markdown com a API Gemini da Google, e exportar o conteúdo final como PDF estilizado no padrão visual do Notion.

---

## ✅ Funcionalidades

- 🎧 **Transcrição de áudio** (`.mp3`, `.wav`, `.m4a`) com timestamps, via Whisper.
- 🧹 **Limpeza do texto** com remoção de stopwords, gerando versão limpa.
- ✍️ **Resumo didático em Markdown** via **API Gemini** (estilo visual do Notion).
- 📄 **Exportação como PDF estilizado**, com títulos e emojis.
- 🧠 **Geração de flashcards Anki** automáticos via `genanki`.
- 📝 **Criação de guias de estudo em PDF**, baseados nos resumos Gemini.
- ❓ **Geração de questões clínicas** em `.pdf` com base no conteúdo da aula.
- 🖼️ **Busca de imagens anatômicas e diagramas** via API externa.
- 🎙️ **Modo escuta profunda**: mesmo com ruídos/barulhos, o sistema tenta extrair o máximo de conteúdo.

---

## 🧭 Visão Geral do Fluxo do MPfSMl

O diagrama abaixo resume de forma clara o funcionamento do MPfSMl — desde a entrada de áudio até a geração dos materiais de estudo automatizados:

![Fluxo do MPfSMl](https://raw.githubusercontent.com/NiedsonEmanoel/MPfSMI/refs/heads/main/aulas_processadas/MPfSML.png)

> O sistema foi pensado para transformar qualquer aula (inclusive aulas ruins) em aprendizado ativo, integrado e automatizado, com mínimo esforço do aluno.

---

## 🚀 Executando com Google Colab

Para facilitar a execução do projeto sem necessidade de instalação local, disponibilizamos um notebook interativo no Google Colab:

[Executar no Google Colab](https://colab.research.google.com/drive/1hcmTnKLOlGSji4GJS7dIMkub6WJRGZ_1?usp=sharing)

**Vantagens do uso do Colab:**

- **Sem instalação necessária:** Execute o código diretamente no navegador.
- **Ambiente pré-configurado:** O Colab já possui diversas bibliotecas instaladas.
- **Acesso a GPUs gratuitas:** O Colab oferece acesso a GPUs para acelerar o processamento.

## 📚 Aprenda a Usar o MPfSMI no Google Colab

Confira a playlist com o passo a passo completo:

[Como Usar o MPfSMI no Google Colab - Playlist no YouTube](LINK_DA_PLAYLIST_AQUI)

Inclui:

- Como carregar e executar o notebook no Colab
- Exemplos práticos de uso
- Dicas para otimizar o desempenho

---

## 🃏 Flashcards para Anki (via Gemini + genanki)

O **MPfSMl** também gera **flashcards automáticos** com base no conteúdo do resumo da aula.

### 🔧 Como funciona:

- O resumo é enviado para a **API Gemini** com prompt específico.
- O retorno vem em **JSON**, com pares **Pergunta/Resposta**.
- Os pares são convertidos para um baralho `.apkg` via [`genanki`](https://github.com/kerrickstaley/genanki).

### 💡 Exemplo:

| Frente (Pergunta)                                           | Verso (Resposta)                                                                 |
|-------------------------------------------------------------|----------------------------------------------------------------------------------|
| Qual é o principal mediador da resposta inflamatória aguda? | A histamina é um dos principais mediadores da resposta inflamatória aguda.      |

### 🧠 Importar no Anki:

1. Após processar a aula, localize o `.apkg` em `aulas_processadas/nome_do_audio/`
2. Abra o Anki > `Arquivo > Importar`
3. Selecione o arquivo

---

## 🚀 Requisitos

### Dependências Python

```bash
pip install openai-whisper torch nltk weasyprint markdown
```

### Dependências Externas

#### 🔊 FFmpeg

- [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

#### 🖼️ GTK3 (para Windows):

- [https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)

#### ⚡ CUDA (Opcional)

```python
import torch
print(torch.cuda.is_available())
```

---

## 🔑 Chave da API Gemini

1. Acesse: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Crie sua chave
3. Crie o arquivo `gemini.key` na raiz do projeto e cole sua chave

> **Importante**: Não compartilhe sua chave.

---

## 📁 Estrutura

```
📂 seu_projeto/
├── script.py
├── gemini.key
├── 📂 aulas_processadas/
│   └── 📂 nome_do_audio/
│       ├── resumo.pdf
│       └── ...
```

---

## 🧠 Como Usar

1. Coloque os áudios na mesma pasta do script.
2. Verifique se `gemini.key` está correto.
3. Execute o script:

### 🎯 Modo rápido

```bash
python transcrever.py 
```

### ⚙️ Modo avançado

```bash
python transcrever.py --audio meuaudio.mp3 --modelo medium 
```

| Flag              | Descrição                                | Valor padrão |
|-------------------|--------------------------------------------|--------------|
| `--modelo`        | Modelo Whisper: `tiny`, `base`, `small`... | `base`       |
| `--audio`         | Nome do arquivo de áudio                   | `none`       |

---

## 🧪 Modelos Whisper

| Modelo   | Tamanho | Qualidade     | Performance     |
|----------|---------|---------------|------------------|
| `tiny`   | Leve    | Baixa         | Muito rápido     |
| `base`   | Médio   | OK            | Rápido           |
| `small`  | Bom     | Boa           | Ok               |
| `medium` | Grande  | Muito boa     | Um pouco lento   |
| `large`  | Enorme  | Excelente     | Lento            |

---

## 📝 Prompt Enviado ao Gemini

> "Sem fornecer nenhum tipo de feedback [...] Texto da transcrição: (transcrição)"

---

## ⚠️ Observações

- O script remove automaticamente marcações extras de Markdown.
- A performance depende do modelo Whisper escolhidp.
- Detecta `cuda` - GPU Nvidia automaticamente.

---

## 📌 Requisitos de Sistema

- Python 3.8+
- Windows
- 8GB+ RAM
---

## 🧼 Limpeza

Todos os arquivos temporários são automaticamente removidos ou movidos para `aulas_processadas/`.

---

## 📜 Licença

Uso educacional/pessoal. Verifique os termos das APIs usadas.

---

## 👨‍💻 Autor

Feito com ☕ e 🧠 por **Niedson Emanoel** — para mim e para todos os estudantes de medicina que amam tecnologia.
