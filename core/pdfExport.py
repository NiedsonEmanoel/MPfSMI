# MPfSMl - Medical Practice for Students on Machine Learning
# Niedson Emanoel, 21/04/2025.
# REFACTORY MADE 03/08/2025

import os
import markdown
import pdfkit
from utilities import load_file_content

def gerar_pdf_markdown(markdown_text, pasta_destino, nome_pdf):
    # markdown_text = preparar_markdown_para_busca(markdown_text) - Markdown já está preparado com as imagens, ja do resume.py
    html_content = markdown.markdown(markdown_text, extensions=["extra", "tables", "fenced_code"])
    full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{load_file_content("../Prompts/notionStyle.css")}</head><body>{html_content}</body></html>"
    caminho_pdf = os.path.join(pasta_destino, nome_pdf)
    options = {
        'page-size': 'A4',  # Tamanho A4
        'margin-top': '2cm',  # Margem superior (ABNT)
        'margin-right': '2cm',  # Margem direita (ABNT)
        'margin-bottom': '2cm',  # Margem inferior (ABNT)
        'margin-left': '2cm',  # Margem esquerda (ABNT)
        'encoding': 'UTF-8',  # Codificação do texto
        'no-outline': None  # Evita que o PDF tenha um contorno (útil para documentos mais limpos)
    }
    pdfkit.from_string(full_html, caminho_pdf, options=options)
    # Gerando o PDF a partir do HTML com as configurações definidas
    print(f"✅ PDF gerado com sucesso: {caminho_pdf}")



