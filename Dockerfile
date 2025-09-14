# ==========================
# Etapa 1: Imagem base com CUDA
# ==========================
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# ==========================
# Etapa 2: Dependências do sistema
# ==========================
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    ffmpeg \
    wkhtmltopdf \
    build-essential \
    libffi-dev \
    libcairo2 \
    pango1.0-tools \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# ==========================
# Etapa 3: Diretório de trabalho
# ==========================
WORKDIR /app

# ==========================
# Etapa 4: Dependências Python
# ==========================
COPY requirements.txt .

# Instalar PyTorch GPU + dependências do projeto
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
RUN pip install --no-cache-dir -r requirements.txt

# ==========================
# Etapa 5: Copiar código
# ==========================
COPY . .

# ==========================
# Etapa 6: Configuração Streamlit
# ==========================
ENV PORT=8080
ENV STREAMLIT_SERVER_PORT=$PORT
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# ==========================
# Etapa 7: Executar
# ==========================
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
