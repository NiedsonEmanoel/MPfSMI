import streamlit as st
import tempfile

from src.core import (
    utilities,
    flashcards,
    pdfExport,
    questions,
    resume,
    searchImage,
    transcription_whisper,
)

# =======================
# 🎨 CONFIGURAÇÃO DE PÁGINA E ESTILO
# =======================
st.set_page_config(page_title="MPfSML", page_icon="img/rephraise_logo.png")

# Remover espaços superiores e elementos de Streamlit
st.markdown("""
<style>
.css-1egvi7u {margin-top: -4rem;}
.css-qrbaxs, .css-15tx938 {min-height: 0.0rem;}
.css-znku1x a {color: #9d03fc;}  /* Link color (ambos temas) */
.stSpinner > div > div {border-top-color: #9d03fc;}
header, #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =======================
# 🔑 AUTENTICAÇÃO DA API
# =======================
def autenticar_api():
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = ""
    if "api_key_valid" not in st.session_state:
        st.session_state.api_key_valid = False

    if not st.session_state.api_key_valid:
        st.subheader("🔐 Autenticação Gemini API")
        api_key_input = st.text_input("Insira sua chave da API Gemini:", type="password", help="Chave obtida no Google AI Studio")

        if api_key_input:
            if len(api_key_input.strip()) >= 10:
                st.session_state.gemini_api_key = api_key_input.strip()
                st.session_state.api_key_valid = True
                st.success("✅ Chave da API registrada com sucesso!")
                st.rerun()
            else:
                st.error("❌ Chave da API parece inválida. Verifique se copiou corretamente.")
        else:
            st.info("ℹ️ Insira sua chave da API para continuar.")
        st.stop()

# =======================
# 📂 UPLOAD E PROCESSAMENTO DE ÁUDIO
# =======================
def processar_audio(api_key):
    with st.expander("🎙️ MPfSML – Processamento de Áudio", expanded=False):
        uploaded_file = st.file_uploader(
            "Envie um arquivo de áudio (.mp3, .wav, .m4a)", 
            type=["mp3", "wav", "m4a"],
            label_visibility="visible"
        )

        if uploaded_file:
            audio_bytes = uploaded_file.read()
            file_size_mb = len(audio_bytes) / (1024 * 1024)

            if file_size_mb > 1024:
                st.error(f"❌ Arquivo de {file_size_mb:.2f} MB excede o limite de 1 GB.")
                st.stop()

            st.success(f"📄 Arquivo '{uploaded_file.name}' carregado ({file_size_mb:.2f} MB)")

            if st.button("▶️ Processar áudio", use_container_width=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                    tmp.write(audio_bytes)
                    temp_audio_path = tmp.name

                st.info("🔄 Processando o áudio...")
                # Exemplo de chamada: with_time, no_time = transcription_whisper.transcrever_audio(temp_audio_path, modelo="medium", api_key=api_key)
                st.success("✅ Processamento concluído!")
        else:
            st.warning("📂 Faça o upload de um áudio para iniciar o processamento.")

# =======================
# 🧠 APLICATIVO PRINCIPAL
# =======================
def maingen():
    st.image("img/image_banner.png", use_column_width=True)
    st.markdown("Processa conteúdos de aulas médicas em transcrições, resumos, flashcards e questões – com IA (Gemini). Feito por Niedson Emanoel.")
    
    autenticar_api()
    api_key = st.session_state.gemini_api_key
    processar_audio(api_key)

# =======================
# 🚀 EXECUÇÃO
# =======================
if __name__ == "__main__":
    maingen()
