from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
driver = webdriver.Chrome(options=chrome_options)

def pegar_imagens_com_selenium(pesquisa):
    query = urllib.parse.quote(pesquisa)
    url = f"https://www.google.com/search?q={query}&udm=2&hl=pt-BR&tbm=isch"

    try:
        driver.get(url)
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
                    div_com_imagem = WebDriverWait(driver, 10).until(
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

                    # Se houver imagens de alta resolução, retorna a lista
                    if links_imagens_alta_resolucao:
                        return links_imagens_alta_resolucao[1]

                except Exception as e:
                    print("Erro ao capturar as imagens de alta qualidade:", e)
                    return []

    finally:
        driver.quit()

# Teste
links = pegar_imagens_com_selenium("dobramento quarta semana embriao")
print(links)
