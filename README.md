# 🎧 Audio to Resume

Este projeto permite transcrever áudios (como aulas, reuniões, entrevistas) usando o modelo [`whisper`](https://github.com/openai/whisper), gerar um resumo didático em Markdown com a API Gemini da Google, e exportar o conteúdo final como PDF estilizado no padrão visual do Notion.

---

## ✅ Funcionalidades

- Transcrição de arquivos de áudio (`.mp3`, `.wav`, `.m4a`) com timestamps.
- Remoção de `stopwords` e geração de versão "limpa" do texto.
- Resumo didático via **Gemini API** da Google.
- Conversão de Markdown para PDF com estilo tipo Notion.
- Limpeza automática de arquivos temporários.

---

## 🚀 Requisitos

### Dependências Python

Instale os seguintes pacotes via `pip`:

```bash
pip install openai-whisper torch nltk weasyprint markdown
```

---

### Dependências Externas

#### 🔊 FFmpeg

Whisper exige o FFmpeg instalado e configurado no PATH.

- Site oficial: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- Para Windows: baixe o executável e adicione o caminho da pasta `bin` nas variáveis de ambiente do sistema.

#### 🖼️ GTK3 para WeasyPrint

WeasyPrint requer o ambiente GTK no Windows.

- Baixe e instale a runtime GTK3:
  - [https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)
- Após a instalação, adicione o diretório `bin` da GTK ao seu PATH.

#### ⚡ CUDA (Opcional)

Caso possua uma GPU NVIDIA, você pode configurar o CUDA para usar o Whisper de forma acelerada:

1. Instale os drivers CUDA + cuDNN compatíveis com sua versão do PyTorch.
2. Verifique se o dispositivo CUDA está disponível com:

```python
import torch
print(torch.cuda.is_available())
```

---

## 🔑 Obtenção da Chave da API Gemini

Para gerar os resumos, você precisará de uma chave de API do Gemini.

### Passos:

1. Acesse o link: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Clique em "Criar chave de API".
3. Copie a chave gerada.
4. Crie um arquivo chamado `gemini.key` (sem aspas) na **pasta raiz do projeto**.
5. Cole a chave dentro deste arquivo, sem espaços extras ou quebras de linha.

> **Importante**: Não compartilhe sua chave com outras pessoas. Ela permite o uso da sua cota de requisições da API.

---

## 📁 Estrutura

```
📂 seu_projeto/
│
├── 📜 script.py
├── 🔑 gemini.key        # Coloque sua chave da API Gemini aqui
├── 📂 aulas_processadas/
│   └── 📂 nome_do_audio/
│       ├── resumo.pdf
│       └── (arquivos temporários removidos ao final)
```

---

## 🧠 Como Usar

1. Coloque os áudios `.mp3`, `.wav` ou `.m4a` na mesma pasta do script.
2. Certifique-se de que o arquivo `gemini.key` contém **apenas** sua chave da API Gemini.
3. Execute o script:

```bash
python script.py
```

4. Escolha o áudio desejado (se houver mais de um).
5. O script irá:
   - Transcrever o áudio com timestamps
   - Gerar uma versão limpa (sem timestamps e sem stopwords)
   - Enviar a transcrição para a API Gemini
   - Gerar um resumo em Markdown
   - Exportar o resumo como PDF estilizado
   - Limpar os arquivos temporários

---

## 📝 Exemplo de Prompt Enviado ao Gemini

> "Sem fornecer nenhum tipo de feedback, comentário ou explicação adicional, gere um resumo completo e didático da transcrição da aula que vou enviar a seguir. O objetivo é facilitar a compreensão de um aluno de medicina, então complemente com informações relevantes sempre que considerar útil para a assimilação do conteúdo.
>
> O resumo deve ser entregue em Markdown puro, como se fosse um código-fonte, com títulos estilizados com emojis, no estilo visual do Notion.
>
> Apenas retorne o conteúdo em Markdown, sem nenhuma outra resposta textual. Texto da transcrição: (transcrição)"

---

## ⚠️ Observações

- A API Gemini pode retornar trechos com blocos de código Markdown encapsulados. O script remove essas marcações automaticamente.
- A performance da transcrição pode variar conforme o modelo Whisper escolhido (`base`, `small`, `medium`, etc.).
- O script detecta automaticamente se você pode usar `cuda` (GPU) ou `cpu`.

---

## 📌 Requisitos de Sistema

- Python 3.8 ou superior
- Sistema operacional Windows (testado)
- Memória recomendada: 8GB+
- Internet ativa (para chamadas à API Gemini)

---

## 🧼 Limpeza

Após a execução, todos os arquivos de áudio, transcrição e Markdown são automaticamente movidos para a pasta `aulas_processadas`.

---

## 💡 To Do

- Incluir a geração de flashcards anki pelo gemini

---

## 📜 Licença

Este projeto é de uso pessoal/educacional. Verifique os termos de uso das APIs utilizadas (Whisper, Gemini, WeasyPrint) antes de distribuir.

---

## 👨‍💻 Autor

Feito com ☕ e 🧠 por Niedson Emanoel, para me ajudar nas aulas de medicina — e agora pode ajudar você também!
