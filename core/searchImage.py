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
# Anatomia e Fisiologia Cardíaca

## 1. Estrutura Macroscópica e Localização do Coração

O coração é um órgão muscular oco, de formato cônico, responsável pelo bombeamento do sangue para todo o corpo.

### 1.1. Localização Anatômica

-   **Posição:** Situado na cavidade torácica, no mediastino médio (espaço entre os dois pulmões).
-   **Orientação:**
    -   Aproximadamente dois terços do órgão estão localizados à esquerda da linha média do esterno.
    -   O ápice cardíaco (ponta inferior) está voltado para baixo, para frente e para a esquerda, geralmente projetando-se no 5º espaço intercostal esquerdo, na linha hemiclavicular.
    -   A base cardíaca (porção superior e posterior) está voltada para trás, para cima e para a direita, sendo o local de entrada e saída dos grandes vasos.

### 1.2. Pericárdio

O coração é envolvido por um saco fibro-seroso de dupla camada chamado pericárdio.

-   **Pericárdio Fibroso (Externo):** Camada mais externa, densa e não elástica.
    -   **Função:** Proteger o coração, ancorá-lo ao mediastino e prevenir a sua dilatação excessiva (estiramento agudo).
-   **Pericárdio Seroso (Interno):** Camada mais interna e delicada, composta por duas lâminas:
    -   **Lâmina Parietal:** Aderida à face interna do pericárdio fibroso.
    -   **Lâmina Visceral (Epicárdio):** Aderida diretamente à superfície do músculo cardíaco (miocárdio).
-   **Cavidade Pericárdica:** Espaço virtual entre as lâminas parietal e visceral, contendo uma pequena quantidade de líquido pericárdico (cerca de 15-50 mL).
    -   **Função do Líquido:** Atua como lubrificante, reduzindo o atrito entre as camadas durante os batimentos cardíacos.
    -   **Contexto Clínico (Derrame Pericárdico):** O acúmulo excessivo de líquido nesta cavidade (derrame pericárdico) pode comprimir o coração, dificultando seu enchimento diastólico e levando a um quadro de **tamponamento cardíaco**.

(IMAGEM: Anatomia do pericárdio mostrando as camadas fibrosa e serosa, e a cavidade pericárdica)

### 1.3. Paredes e Câmaras Cardíacas

A parede do coração é composta por três camadas:

-   **Epicárdio (externo):** Lâmina visceral do pericárdio seroso.
-   **Miocárdio (médio):** Camada muscular espessa, formada por tecido muscular estriado cardíaco. É a camada funcional responsável pela contração (sístole). A espessura do miocárdio varia entre as câmaras, sendo mais espessa no ventrículo esquerdo devido à maior pressão que ele precisa gerar.
-   **Endocárdio (interno):** Camada fina de endotélio que reveste o interior das câmaras cardíacas e as valvas. É contínuo com o endotélio dos vasos sanguíneos.

O coração é dividido em quatro câmaras:

-   **Dois Átrios (superiores):** Câmaras de recepção de sangue.
    -   **Átrio Direito:** Recebe sangue venoso (pobre em oxigênio) da circulação sistêmica através das veias cavas superior e inferior, e do seio coronário (drenagem venosa do próprio coração).
    -   **Átrio Esquerdo:** Recebe sangue arterial (rico em oxigênio) da circulação pulmonar através das quatro veias pulmonares.
-   **Dois Ventrículos (inferiores):** Câmaras de ejeção de sangue.
    -   **Ventrículo Direito:** Bombeia sangue venoso para os pulmões através do tronco pulmonar.
    -   **Ventrículo Esquerdo:** Bombeia sangue arterial para todo o corpo através da artéria aorta. Possui a parede miocárdica mais espessa (aproximadamente 3x mais espessa que a do ventrículo direito).

(IMAGEM: Corte coronal do coração humano mostrando as quatro câmaras, o septo interventricular e a espessura relativa do miocárdio)

## 2. Valvas Cardíacas

As valvas cardíacas são estruturas de tecido conjuntivo denso, recobertas por endocárdio, que garantem o fluxo unidirecional do sangue através do coração, abrindo e fechando passivamente em resposta aos gradientes de pressão.

### 2.1. Valvas Atrioventriculares (AV)

Localizadas entre os átrios e os ventrículos.

-   **Valva Tricúspide:** Entre o átrio direito e o ventrículo direito. Possui três cúspides (folhetos).
-   **Valva Mitral (ou Bicúspide):** Entre o átrio esquerdo e o ventrículo esquerdo. Possui duas cúspides.

As cúspides das valvas AV estão ancoradas às paredes ventriculares pelos **músculos papilares** através de filamentos tendíneos chamados **cordas tendíneas**.

-   **Função do Aparelho Subvalvar (Músculos Papilares + Cordas Tendíneas):** Durante a sístole ventricular, a contração dos músculos papilares tensiona as cordas tendíneas, impedindo que as cúspides sofram prolapso (evertam) para dentro dos átrios sob alta pressão.

### 2.2. Valvas Semilunares (SL)

Localizadas na saída dos ventrículos para os grandes vasos.

-   **Valva Pulmonar:** Na saída do ventrículo direito para o tronco pulmonar.
-   **Valva Aórtica:** Na saída do ventrículo esquerdo para a artéria aorta.

Ambas são compostas por três cúspides em formato de "meia-lua" e não possuem cordas tendíneas ou músculos papilares. Seu fechamento ocorre passivamente quando a pressão nos grandes vasos (aorta e tronco pulmonar) excede a pressão nos ventrículos, ao final da sístole.

(IMAGEM: Valvas cardíacas em vista superior com o coração seccionado, mostrando a tricúspide, mitral, aórtica e pulmonar)

## 3. Sistema de Condução Elétrica do Coração

O coração possui um sistema especializado de células musculares cardíacas modificadas (não-contráteis) que geram e conduzem impulsos elétricos de forma autônoma, coordenando as contrações das câmaras.

### 3.1. Componentes do Sistema de Condução

1.  **Nó Sinoatrial (SA) ou Nó de Keith-Flack:**
    -   **Localização:** Parede póstero-lateral superior do átrio direito, próximo à abertura da veia cava superior.
    -   **Função:** É o **marcapasso natural** do coração. Possui a maior taxa de despolarização espontânea (automatismo), gerando impulsos em uma frequência de **60 a 100 batimentos por minuto (bpm)** em repouso.
2.  **Vias Internodais:** Feixes de condução que propagam o impulso do nó SA para o nó AV através dos átrios.
3.  **Nó Atrioventricular (AV) ou Nó de Aschoff-Tawara:**
    -   **Localização:** No septo interatrial, próximo à valva tricúspide.
    -   **Função:** Recebe o impulso do nó SA e promove um **atraso fisiológico na condução** (aproximadamente 0.1 segundo). Esse atraso é crucial, pois permite que os átrios se contraiam completamente e ejetem seu sangue para os ventrículos antes que a contração ventricular comece.
4.  **Feixe de His (Feixe Atrioventricular):**
    -   **Função:** É a única conexão elétrica entre os átrios e os ventrículos. Perfura o esqueleto fibroso do coração (que isola eletricamente as câmaras).
5.  **Ramos Direito e Esquerdo do Feixe:**
    -   O feixe de His se divide em dois ramos que descem pelo septo interventricular.
6.  **Fibras de Purkinje:**
    -   **Função:** Rede terminal de fibras que se ramificam a partir dos ramos do feixe e se espalham pelo miocárdio ventricular, distribuindo o impulso elétrico rapidamente para as células musculares ventriculares e garantindo uma contração sincronizada e eficiente, de baixo para cima (do ápice para a base).

(IMAGEM: Diagrama do sistema de condução elétrica do coração, mostrando o nó SA, nó AV, feixe de His, ramos e fibras de Purkinje)

## 4. O Ciclo Cardíaco

O ciclo cardíaco compreende todos os eventos elétricos e mecânicos que ocorrem no coração durante um batimento completo. É dividido em duas fases principais: **sístole** (contração) e **diástole** (relaxamento).

### 4.1. Fases do Ciclo Cardíaco (Lado Esquerdo como Referência)

| Fase | Evento Elétrico (ECG) | Valvas | Descrição Mecânica |
| :--- | :--- | :--- | :--- |
| **Diástole Ventricular** | | | **Fase de Enchimento Ventricular** |
| 1. Enchimento Rápido | Final da Onda T | Mitral: Aberta<br>Aórtica: Fechada | O ventrículo relaxa e sua pressão cai abaixo da pressão atrial. A valva mitral se abre passivamente e o sangue flui rapidamente do átrio para o ventrículo (aprox. 80% do enchimento). |
| 2. Diástase | - | Mitral: Aberta<br>Aórtica: Fechada | O enchimento ventricular diminui à medida que as pressões atrial e ventricular se equalizam. |
| 3. Contração Atrial | Onda P | Mitral: Aberta<br>Aórtica: Fechada | O nó SA dispara, os átrios se contraem (**sístole atrial**) e ejetam o volume final de sangue para os ventrículos (aprox. 20% restantes). O volume no ventrículo ao final da diástole é o **Volume Diastólico Final (VDF)**. |
| **Sístole Ventricular** | | | **Fase de Ejeção Ventricular** |
| 4. Contração Isovolumétrica | Complexo QRS | Mitral: Fechada<br>Aórtica: Fechada | Os ventrículos começam a contrair. A pressão ventricular aumenta rapidamente, excedendo a pressão atrial e causando o **fechamento da valva mitral (primeira bulha cardíaca - B1)**. Como a pressão ainda não superou a aórtica, a valva aórtica permanece fechada. O volume ventricular não se altera. |
| 5. Ejeção Rápida | - | Mitral: Fechada<br>Aórtica: Aberta | A pressão ventricular excede a pressão na aorta, forçando a **abertura da valva aórtica**. O sangue é ejetado rapidamente para a aorta. |
| 6. Ejeção Lenta | Início da Onda T | Mitral: Fechada<br>Aórtica: Aberta | A ejeção continua, mas de forma mais lenta, à medida que a pressão ventricular começa a cair. |
| **Início da Diástole** | | | **Fase de Relaxamento Ventricular** |
| 7. Relaxamento Isovolumétrico | Final da Onda T | Mitral: Fechada<br>Aórtica: Fechada | Os ventrículos relaxam. A pressão ventricular cai abaixo da pressão aórtica, causando o **fechamento da valva aórtica (segunda bulha cardíaca - B2)**. Ambas as valvas (mitral e aórtica) estão fechadas. O volume ventricular não se altera, correspondendo ao **Volume Sistólico Final (VSF)**. O ciclo recomeça quando a pressão ventricular cai abaixo da atrial. |

### 4.2. Débito Cardíaco (DC)

O Débito Cardíaco é o volume de sangue bombeado pelo ventrículo esquerdo (ou direito) em um minuto. É um indicador fundamental da função cardíaca.

**Fórmula:**
`Débito Cardíaco (DC) = Frequência Cardíaca (FC) x Volume Sistólico (VS)`

-   **Frequência Cardíaca (FC):** Número de batimentos por minuto (bpm).
-   **Volume Sistólico (VS):** Volume de sangue ejetado por um ventrículo a cada batimento.
    -   `VS = Volume Diastólico Final (VDF) - Volume Sistólico Final (VSF)`

**Fatores que Influenciam o Débito Cardíaco:**

1.  **Pré-carga:** Grau de estiramento do músculo ventricular ao final da diástole (relacionado ao VDF).
    -   **Lei de Frank-Starling:** Dentro de limites fisiológicos, quanto maior a pré-carga (maior o enchimento ventricular), maior será a força de contração e, consequentemente, maior o volume sistólico.
2.  **Pós-carga:** A resistência que o ventrículo precisa vencer para ejetar o sangue.
    -   No ventrículo esquerdo, a pós-carga é representada principalmente pela pressão arterial sistêmica.
    -   Aumentos na pós-carga (ex: hipertensão arterial) dificultam a ejeção, podendo diminuir o volume sistólico.
3.  **Contratilidade (Inotropismo):** Força intrínseca de contração do miocárdio, independente da pré-carga.
    -   Pode ser aumentada por estímulos do sistema nervoso simpático (ex: adrenalina) e fármacos (ex: digitálicos).
    -   Pode ser diminuída em condições como infarto do miocárdio ou insuficiência cardíaca.
"""

# Aplicar a função
markdown_final = preparar_markdown_para_busca(markdown_original)

print(markdown_final)
