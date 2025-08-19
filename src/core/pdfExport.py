# MPfSMl - Medical Practice for Students on Machine Learning
# Niedson Emanoel, 21/04/2025.
# REFACTORY MADE 03/08/2025

import os
import markdown
import pdfkit
from .utilities import load_file_content
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
data_hoje = datetime.today().strftime('%d/%m/%Y')

def gerar_pdf_markdown(markdown_text, pasta_destino, nome_pdf):
    # Define o caminho do PDF a ser gerado
    caminho_pdf = os.path.join(pasta_destino, nome_pdf)
    rodape_texto = (
        f"Niedson Emanoel - MPfSML - "
        f"TURMA XXXIX MEDICINA UNIVASF PNZ - {data_hoje}"
    )

    # Converte markdown para HTML
    html_content = markdown.markdown(markdown_text, extensions=["extra", "tables", "fenced_code"])
    
    css_content = load_file_content('notionStyle.css',"prompt do css")
    
    full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css_content}</style></head><body>{html_content}</body></html>"

    # Opções de formatação do PDF
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'no-outline': None,
        'footer-center': rodape_texto,
        'footer-font-size': '9'
    }

    try:
        if os.name == 'nt':
            # Caminho absoluto baseado na pasta deste arquivo (pdfExport.py)
            base_dir = os.path.dirname(os.path.abspath(__file__))
            wkhtmltopdf_path = os.path.join(base_dir, '..', 'binaries', 'wkhtmltopdf_winX86', 'bin', 'wkhtmltopdf.exe')
            wkhtmltopdf_path = os.path.abspath(wkhtmltopdf_path)

            if not os.path.exists(wkhtmltopdf_path):
                raise FileNotFoundError(f"Binário do wkhtmltopdf não encontrado em: {wkhtmltopdf_path}")

            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            pdfkit.from_string(full_html, caminho_pdf, options=options, configuration=config)
        else:
            # Para Linux (ex: servidores ou Colab)
            #config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
            pdfkit.from_string(full_html, caminho_pdf, options=options, configuration=config)

        logger.info(f"✅ PDF gerado com sucesso: {caminho_pdf}")
    
    except Exception as e:
        logger.error(f"❌ Erro ao gerar PDF: {e}")
