import streamlit as st
import tempfile
import os
import zipfile

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
    with st.expander("🎙️ MPfSML – Processamento de Áudio", expanded=True):

        uploaded_file = st.file_uploader(
            "Envie um arquivo de áudio (.mp3, .wav, .m4a)", 
            type=["mp3", "wav", "m4a"],
            label_visibility="visible"
        )

        option_map = {
            "tiny": ":material/looks_one: tiny",
            "base": ":material/looks_two: base",
            "small": ":material/looks_3: small",
            "medium": ":material/looks_4: medium",
            "large": ":material/looks_5: large",
        }

        selection = st.segmented_control(
            "Escolha o modelo Whisper",
            options=list(option_map.keys()),
            format_func=lambda opt: option_map[opt],
            selection_mode="single",
            default="base"
        )

        modelo = selection if selection else "base"

        if uploaded_file:
            audio_bytes = uploaded_file.read()
            file_size_mb = len(audio_bytes) / (1024 * 1024)

            if file_size_mb > 1024:
                st.error(f"❌ Arquivo de {file_size_mb:.2f} MB excede o limite de 1 GB.")
                st.stop()

            if st.button("▶️ Processar áudio", use_container_width=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                    audioname = uploaded_file.name.split('.')[0]
                    tmp.write(audio_bytes)
                    temp_audio_path = tmp.name

                with st.status('🔄 Processando o áudio...', expanded=True) as status:
                    st.write("Transcrevendo o áudio...")
                    with_time, no_time = transcription_whisper.transcrever_audio(temp_audio_path, modelo=modelo)
                    
                    # Caminhos temporários para os arquivos gerados
                    temp_dir = tempfile.mkdtemp()
                    resumo_pdf = os.path.join(temp_dir, 'resumo.pdf')
                    questoes_pdf = os.path.join(temp_dir, 'questoes.pdf')
                    flashcards_apkg = os.path.join(temp_dir, f'{audioname}.apkg')

                    st.write("Criando resumo...")
                    resume_markdown = resume.generate_resume(transcricao=no_time, apikey=api_key)
                    pdfExport.gerar_pdf_markdown(resume_markdown, pasta_destino=temp_dir, nome_pdf='resumo.pdf')
                    
                    st.write("Criando questões...")
                    questions_markdown = questions.generate_questions(transcricao=no_time, apikey=api_key)
                    pdfExport.gerar_pdf_markdown(questions_markdown, pasta_destino=temp_dir, nome_pdf='questoes.pdf')  
                     
                    st.write("Criando flashcards...")
                    jsonFlashcards = flashcards.gerarFlashcards(resumo=no_time, apikey=api_key)
                    flashcards.criar_baralho(jsonFlashcards, nome_baralho=os.path.join(temp_dir, audioname))
                    
                    # Compactar em ZIP
                    zip_path = os.path.join(temp_dir, f"{audioname}_materiais.zip")
                    with zipfile.ZipFile(zip_path, 'w') as zipf:
                        zipf.write(resumo_pdf, 'resumo.pdf')
                        zipf.write(questoes_pdf, 'questoes.pdf')
                        zipf.write(flashcards_apkg, f'{audioname}.apkg')

                    status.update(
                        label="✅ Processamento concluído!",
                        state="complete",
                        expanded=False
                    )

                    # Botão de download
                    with open(zip_path, "rb") as f:
                        st.download_button(
                            label="📥 Baixar materiais (ZIP)",
                            data=f,
                            file_name=f"{audioname}_materiais.zip",
                            mime="application/zip"
                        )

                    # Limpeza final dos arquivos temporários
                   
                    os.remove(temp_audio_path)
                    os.remove(resumo_pdf)
                    os.remove(questoes_pdf)
                    os.remove(flashcards_apkg)
                    os.remove(zip_path)
                    os.rmdir(temp_dir)
                

        else:
            st.badge("📂 Faça o upload de um áudio para iniciar o processamento.")
# =======================
# 🧠 APLICATIVO PRINCIPAL
# =======================
def maingen():
    st.image("img/image_banner.png", use_container_width=True)
    st.markdown("Processa conteúdos de aulas médicas em transcrições, resumos, flashcards e questões – com IA (Gemini).")
    
    autenticar_api()
    api_key = st.session_state.gemini_api_key
    processar_audio(api_key)

# =======================
# 🚀 EXECUÇÃO
# =======================
if __name__ == "__main__":
    maingen()
