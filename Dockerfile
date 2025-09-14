# Imagem base com compatibilidade com wkhtmltopdf .deb
FROM python:3.12-buster

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        ffmpeg \
        ca-certificates \
        libxrender1 \
        libfontconfig1 \
        libjpeg62-turbo \
        xfonts-base \
        xfonts-75dpi \
        fonts-dejavu \
    && curl -LO https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb \
    && rm wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt-get remove --purge -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos da aplicação
COPY . .

# Instala dependências Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Streamlit
EXPOSE 8080

# Verifica se o app está rodando
HEALTHCHECK CMD curl --fail http://localhost:8080 || exit 1

# Executa o aplicativo com Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
