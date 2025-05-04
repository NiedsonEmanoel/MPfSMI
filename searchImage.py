from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import time
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
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

markdown_original = """
# 🧠 **Fisiologia Digestória**

## 📚 **Introdução ao Sistema Digestório**
O sistema digestório é responsável pela **digestão**, **absorção** e **eliminação** dos alimentos. Ele é composto por uma série de órgãos, que incluem a boca, esôfago, estômago, intestinos (delgado e grosso), fígado, pâncreas e vesícula biliar.

## 🍽️ **Funções Principais**
1. **Digestão mecânica**: Processo de quebra física dos alimentos.
   - A mastigação, o peristaltismo e a segmentação são exemplos de digestão mecânica.

2. **Digestão química**: Enzimas quebram os macronutrientes em compostos menores.
   - **Amilase** quebra carboidratos, **lipase** quebra lipídios e **protease** quebra proteínas.

3. **Absorção**: Nutrientes são absorvidos no intestino delgado, sendo transportados para o sangue.

4. **Eliminação**: Resíduos não digeridos são eliminados pelo reto.

## 🍞 **Processo Digestivo**

### 🦷 **Boca e Faringe**
- A **mastigação** quebra os alimentos em partículas menores.
- **Saliva** contém **amilase salivar**, iniciando a digestão dos carboidratos.
- A **deglutição** empurra o alimento da boca para a faringe e esôfago.

(IMAGEM: "Diagrama da boca e faringe com destaque para a amilase salivar")

### 🍝 **Esôfago**
- O esôfago é responsável por conduzir o alimento até o estômago através do **peristaltismo**, que são movimentos musculares coordenados.

(IMAGEM: "Esôfago e movimentos peristálticos")

### 🍖 **Estômago**
- O estômago realiza a **digestão mecânica** e **química**.
- As **células parietais** secretam **ácido clorídrico (HCl)**, que ativa a **pepsina**, enzima responsável pela digestão de proteínas.
- **Fatores de proteção**: muco gástrico protege a parede do estômago contra a ação do HCl.

(IMAGEM: "Esquema do estômago com destaque para células parietais e pepsina")

### 🍴 **Intestino Delgado**
- **Duodeno**: Primeira parte do intestino delgado, onde o pâncreas secreta **enzimas digestivas** e o fígado secreta **bile**.
- A bile emulsifica os lipídios, facilitando a ação da lipase.
- **Jejuno e íleo**: Absorção dos nutrientes.

(IMAGEM: "Diagrama do intestino delgado com destaque para duodeno, jejuno e íleo")

### 🧴 **Pâncreas e Fígado**
- O **pâncreas** secreta enzimas como **amilase, lipase** e **protease**, além de **bicarbonato** para neutralizar o pH ácido do quimo vindo do estômago.
- O **fígado** produz **bile**, que é armazenada na **vesícula biliar** e liberada no duodeno para emulsificação de lipídios.

(IMAGEM: "Pâncreas e fígado com destaque para secreção de bile e enzimas digestivas")

### 🦠 **Absorção Intestinal**
- O **intestino delgado** possui vilosidades que aumentam a área de absorção.
- **Microssomos intestinais** e **transportadores específicos** ajudam na absorção de **carboidratos, lipídios e proteínas**.

(IMAGEM: "Esquema do intestino delgado com destaque para vilosidades e células absorventes")

### 🧑‍⚕️ **Regulação da Digestão**
A digestão é regulada por mecanismos **hormonais** e **nervosos**:
- **Gastrina**: Estimula a secreção de ácido gástrico.
- **Colecistocinina (CCK)**: Estimula a liberação de bile e enzimas pancreáticas.
- **Secretina**: Estimula a liberação de bicarbonato pelo pâncreas.
- **Sistema nervoso entérico**: Controla o peristaltismo e a secreção de enzimas.

(IMAGEM: "Diagrama de regulação hormonal da digestão com destaque para gastrina, CCK e secretina")

## 💪 **Absorção de Nutrientes**

### 🥕 **Carboidratos**
- São quebrados em **monossacarídeos** (como glicose) pelas enzimas digestivas.
- Absorção através dos transportadores no intestino delgado.

### 🍖 **Proteínas**
- As proteínas são quebradas em **aminoácidos** pelas proteases (como a pepsina e tripsina).

### 🧈 **Lipídios**
- São digeridos pela **lipase** e absorvidos em forma de **ácidos graxos** e **monoglicerídeos**.

(IMAGEM: "Esquema da absorção de carboidratos, proteínas e lipídios no intestino delgado")

## 🚽 **Eliminação**
- O que não é absorvido no intestino delgado é transportado para o **intestino grosso**, onde ocorre a absorção de água e a formação das fezes.
- As fezes são eliminadas pelo **reto** e **ânus**.

(IMAGEM: "Esquema do intestino grosso e do processo de formação e eliminação de fezes")
"""

# Aplicar a função
markdown_final = preparar_markdown_para_busca(markdown_original)

print(markdown_final)
