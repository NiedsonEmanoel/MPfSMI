from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chromePath
driver = webdriver.Chrome(options=chrome_options)

def pegar_imagens_com_selenium(pesquisa):
    query = urllib.parse.quote(pesquisa)
    url = f"https://www.google.com/search?q={query}&udm=2&hl=pt-BR&tbm=isch"

    try:
        # Abrir uma nova aba para cada busca
        driver.execute_script(f"window.open('{url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])  # Mudar para a nova aba
        time.sleep(2)

        # Encontra todas as imagens de pré-visualização
        imagens = driver.find_elements(By.TAG_NAME, "img")

        links = []
        # Procura pelos links das imagens
        for i, img in enumerate(imagens):
            src = img.get_attribute("src") or img.get_attribute("data-src")
            if src:
                links.append(src)

        # Encontrar o índice do logo do Google (caso exista)
        l = 0
        for i, link in enumerate(links):
            if link == 'https://fonts.gstatic.com/s/i/productlogos/googleg/v6/24px.svg':
                l = i  # Encontramos a posição do logo do Google

        # Pega o link da imagem que deve ser clicada
        link_imagem = links[l + 1] if len(links) > l + 1 else links[0]

        # Agora, vamos interagir com a imagem usando o link
        for img in imagens:
            src = img.get_attribute("src") or img.get_attribute("data-src")
            if src == link_imagem:
                img.click()
                time.sleep(2)  # Espera para a imagem abrir

                # Espera até que a <div> com jscontroller="luWJre" esteja visível
                try:
                    # Localiza a <div> que contém a imagem de alta resolução
                    div_com_imagem = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jscontroller="luWJre"]'))
                    )

                    # Dentro dessa <div>, encontra todas as imagens com a URL de alta qualidade
                    imagens_alta_resolucao = div_com_imagem.find_elements(By.TAG_NAME, 'img')

                    # Captura os links das imagens de alta qualidade
                    links_imagens_alta_resolucao = []
                    for imagem in imagens_alta_resolucao:
                        imagem_src = imagem.get_attribute("src")
                        if imagem_src and imagem_src != src:
                            links_imagens_alta_resolucao.append(imagem_src)

                    # Se houver imagens de alta resolução, retorna o primeiro link
                    if links_imagens_alta_resolucao:
                        return links_imagens_alta_resolucao[1]

                except Exception as e:
                    print("Erro ao capturar as imagens de alta qualidade:", e)
                    return []
    finally:
        print('Imagem ok.')

# Função para preparar o markdown e buscar as imagens
def preparar_markdown_para_busca(texto_markdown):
    def substituir(match):
        descricao = match.group(1).strip()
        link = pegar_imagens_com_selenium(descricao)  # Chama a função para pegar o link da imagem
        if link:
            # Substitui pelo markdown de imagem usando a descrição como alt text e o link da imagem
            return f"![{descricao}]({link})"
        return f"![{descricao}](sem_imagem_disponivel.png)"  # Caso não encontre uma imagem
    
    novo_markdown = re.sub(r"\(IMAGEM:\s*(.*?)\)", substituir, texto_markdown)
    driver.quit()
    return novo_markdown

if __name__ == "__main__":
    markdown_original = """
    # Anatomia do Coração

    (IMAGEM: anatomia externa do coração humano, visão anterior)

    O coração humano é um órgão muscular...

    (IMAGEM: artérias coronárias em dissecção anatômica)
    """

    # Aplicar a função
    markdown_final = preparar_markdown_para_busca(markdown_original)

    print(markdown_final)
