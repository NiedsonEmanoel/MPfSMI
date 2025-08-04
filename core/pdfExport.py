# MPfSMl - Medical Practice for Students on Machine Learning
# Niedson Emanoel, 21/04/2025.
# REFACTORY MADE 03/08/2025

import os
import markdown
import pdfkit
from utilities import load_file_content
import logging
import os
import markdown
from weasyprint import HTML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def gerar_pdf_markdown(markdown_text, pasta_destino, nome_pdf):
    # Define o caminho do PDF a ser gerado
    caminho_pdf = os.path.join(pasta_destino, nome_pdf)
    
    # Converte markdown para HTML
    html_content = markdown.markdown(markdown_text, extensions=["extra", "tables", "fenced_code"])
    full_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{load_file_content('../Prompts/notionStyle.css')}</head><body>{html_content}</body></html>"

    # Opções de formatação do PDF
    options = {
        'page-size': 'A4',
        'margin-top': '2cm',
        'margin-right': '2cm',
        'margin-bottom': '2cm',
        'margin-left': '2cm',
        'encoding': 'UTF-8',
        'no-outline': None
    }

    # Se for Linux, define o caminho manualmente
    if os.name == 'nt':
        config = pdfkit.configuration(wkhtmltopdf='../binaries/wkhtmltopdf_winX86/bin/wkhtmltopdf')
        pdfkit.from_string(full_html, caminho_pdf, options=options, configuration=config)
    else:
        pdfkit.from_string(full_html, caminho_pdf, options=options)

    print(f"✅ PDF gerado com sucesso: {caminho_pdf}")



gerar_pdf_markdown("""

# Coração: Resumo Técnico e Didático

## 1. Introdução e Considerações Gerais

O coração é um órgão muscular oco, de formato cônico, que funciona como uma bomba contrátil e aspirante. Sua principal função é impulsionar o sangue através do sistema circulatório para suprir as necessidades metabólicas de todos os tecidos do corpo.

- **Localização**: Mediastino médio, sobre o diafragma, atrás do esterno e das cartilagens costais, e à frente da coluna vertebral torácica.
- **Posição**: O coração não é posicionado verticalmente no tórax. Ele sofre uma **roto-translação** durante o desenvolvimento embriológico, resultando em:
    - **Eixo maior (ápice-base)**: Oblíquo, direcionado para baixo, para frente e para a esquerda.
    - **Ápice cardíaco**: Formado predominantemente pelo ventrículo esquerdo (VE), localiza-se no nível do 5º espaço intercostal esquerdo, na linha hemiclavicular. É o local de ausculta do **ictus cordis** (pulsação apical).
    - **Base cardíaca**: Formada principalmente pelos átrios, com o átrio esquerdo (AE) sendo o mais posterior. A base é o ponto de fixação dos grandes vasos (aorta, tronco pulmonar, veias cavas e veias pulmonares).
- **Projeção em Relação aos Ventrículos**:
    - **Ventrículo Direito (VD)**: É a câmara mais anterior, localizada logo atrás do esterno.
    - **Ventrículo Esquerdo (VE)**: É mais posterior e lateral esquerdo em relação ao VD.

![Posição do coração no mediastino com projeção das câmaras cardíacas](https://www.kenhub.com/thumbor/j4oqQcWLSFa7BSHpwZ6_BHsjBjo=/fit-in/800x1600/filters:watermark(/images/logo_url.png,-10,-10,0):background_color(FFFFFF):format(jpeg)/images/library/11015/912_Mediastinum__Left_lateral_view.png)

### 1.1. Pericárdio

O coração é envolvido por um saco fibro-seroso de parede dupla chamado pericárdio, que o protege e o ancora no mediastino.

- **Pericárdio Fibroso**: Camada externa, mais resistente e espessa, composta por tecido conjuntivo denso. Prende-se ao diafragma (ligamento pericardicofrênico) e ao esterno (ligamentos esternopericárdicos), limitando a distensão cardíaca excessiva.
- **Pericárdio Seroso**: Camada interna, dividida em duas lâminas:
    - **Lâmina Parietal**: Aderida à face interna do pericárdio fibroso.
    - **Lâmina Visceral (Epicárdio)**: Aderida diretamente à superfície do miocárdio.
- **Cavidade Pericárdica**: Espaço virtual entre as lâminas parietal e visceral, contendo uma fina película de líquido seroso (cerca de 20-50 mL). Este líquido atua como lubrificante, reduzindo o atrito durante os batimentos cardíacos.
    - **Contexto Clínico**: O acúmulo excessivo de líquido nesta cavidade (derrame pericárdico) pode levar ao **tamponamento cardíaco**, uma condição grave onde a compressão externa impede o enchimento diastólico adequado do coração.

![Camadas do pericárdio e parede cardíaca](https://static.mundoeducacao.uol.com.br/mundoeducacao/2023/11/anatomia-pericardio.png)

### 1.2. Seios do Pericárdio

São espaços formados pelas reflexões (dobras) do pericárdio seroso ao redor dos grandes vasos da base do coração.

- **Seio Transverso do Pericárdio**: Passagem posterior à aorta ascendente e ao tronco pulmonar, e anterior à veia cava superior.
    - **Importância Cirúrgica**: Permite o pinçamento temporário (clampeamento) da aorta e do tronco pulmonar durante cirurgias cardíacas, isolando a circulação arterial sistêmica e pulmonar.
- **Seio Oblíquo do Pericárdio**: Fundo de saco em forma de "J" invertido, localizado posteriormente ao átrio esquerdo, delimitado pela chegada das veias cavas e pulmonares.

![Seio transverso e seio oblíquo do pericárdio](https://cdn1.imaios.com/i/imaios-images/web/images/eanatomy/modules/coeur-illustrations/images/v1/8bec5f70ad8499d14af9e6fba82a594283309116ae70a47fdc7b1169752e901a?ar=640:670&bg=FFFFFF&fit=crop&p64=MTA5Niw2MzI&t=U2VpbyBvYmzDrXF1byBkbyBwZXJpY8OhcmRpbw&tx=1096&ty=632&w=350&wk=1&s=43d08681218f169c56fa8d898cd16eec)

## 2. Anatomia Macroscópica e Estrutura Cardíaca

### 2.1. Configuração Externa

A superfície do coração é marcada por sulcos que indicam a separação entre as câmaras e abrigam os principais vasos coronarianos e tecido adiposo.

- **Sulco Coronário (ou Atrioventricular)**: Circunda o coração, separando os átrios dos ventrículos.
- **Sulcos Interventriculares (Anterior e Posterior)**: Marcam a localização do septo interventricular na superfície externa, separando os ventrículos direito e esquerdo.
- **Faces do Coração**:
    - **Face Esternocostal (Anterior)**: Formada principalmente pelo VD.
    - **Face Diafragmática (Inferior)**: Formada majoritariamente pelo VE e uma porção do VD, repousa sobre o diafragma.
    - **Face Pulmonar (Esquerda)**: Formada pelo VE, voltada para o pulmão esquerdo.

### 2.2. Câmaras Cardíacas

O coração é composto por quatro câmaras: dois átrios (câmaras de recepção) e dois ventrículos (câmaras de ejeção).

#### 2.2.1. Átrio Direito (AD)

Recebe sangue venoso (pobre em oxigênio) do corpo através de três vasos principais:
- **Veia Cava Superior (VCS)**: Drena sangue da parte superior do corpo (cabeça, pescoço, membros superiores).
- **Veia Cava Inferior (VCI)**: Drena sangue da parte inferior do corpo (abdome, pelve, membros inferiores).
- **Seio Coronário**: Drena o sangue venoso do próprio miocárdio.

**Estruturas Internas do Átrio Direito:**

| Estrutura | Descrição e Função | Contexto Embriológico/Clínico |
| :--- | :--- | :--- |
| **Aurícula Direita** | Expansão sacular na porção anterior do átrio, com paredes rugosas devido aos **músculos pectíneos**. Aumenta a capacidade volumétrica do átrio. | A estase sanguínea na aurícula, comum em fibrilação atrial, é um local frequente de formação de trombos. |
| **Crista Terminal** | Marco muscular proeminente que separa a porção lisa (Sinus Venarum) da porção rugosa (átrio propriamente dito). | Corresponde ao local de origem embriológica do seio venoso. O nó sinoatrial (SA) localiza-se na porção superior da crista. |
| **Óstio do Seio Coronário** | Abertura do seio coronário, geralmente protegida por uma prega rudimentar, a **válvula de Tebésio**. | - |
| **Válvula da VCI (de Eustáquio)** | Prega de tecido que, no feto, direciona o sangue oxigenado da VCI para o forame oval. Em adultos, é rudimentar. | - |
| **Septo Interatrial** | Parede que separa o AD do AE. Apresenta a **fossa oval**. | A fossa oval é um remanescente do **forame oval**, uma comunicação interatrial essencial na circulação fetal que se fecha após o nascimento. A persistência (Forame Oval Patente) é uma anomalia congênita. |
| **Óstio Atrioventricular Direito** | Abertura que comunica o AD com o VD, guardada pela **valva tricúspide**. | - |

#### 2.2.2. Ventrículo Direito (VD)

Recebe sangue do AD e o bombeia para os pulmões através do tronco pulmonar. Sua parede é mais fina que a do VE, pois trabalha contra a baixa resistência da circulação pulmonar.

**Estruturas Internas do Ventrículo Direito:**

- **Via de Entrada**: Caracterizada pela presença da valva tricúspide e de múltiplas trabéculas cárneas.
- **Via de Saída (Cone Arterial ou Infundíbulo)**: Porção superior, lisa, que leva ao tronco pulmonar.
- **Trabéculas Cárneas**: Feixes musculares irregulares que revestem a maior parte da parede ventricular.
- **Músculos Papilares**: Projeções musculares cônicas (anterior, posterior e septal) que se ligam às cúspides da valva tricúspide através das **cordas tendíneas**. A contração desses músculos durante a sístole ventricular previne o prolapso (eversão) das cúspides para o átrio.
- **Trabécula Septomarginal (Banda Moderadora)**: Feixe muscular proeminente que cruza do septo interventricular até a base do músculo papilar anterior. Contém parte do ramo direito do feixe de His, importante para a condução do impulso elétrico.
- **Crista Supraventricular**: Crista muscular que separa a via de entrada da via de saída do VD.

#### 2.2.3. Átrio Esquerdo (AE)

Recebe sangue arterial (rico em oxigênio) dos pulmões através das **quatro veias pulmonares** (duas superiores e duas inferiores). É a câmara mais posterior do coração.

- **Estrutura**: A maior parte de sua parede interna é lisa. A **aurícula esquerda**, similar à direita, possui músculos pectíneos.
- **Óstio Atrioventricular Esquerdo**: Comunica o AE com o VE, guardado pela **valva mitral (ou bicúspide)**.

#### 2.2.4. Ventrículo Esquerdo (VE)

Recebe sangue do AE e o bombeia para todo o corpo através da aorta.

- **Estrutura**:
    - **Parede Muscular**: É de 2 a 3 vezes mais espessa que a do VD, refletindo a alta pressão e resistência da circulação sistêmica.
    - **Cavidade**: Mais longa e cônica que a do VD.
    - **Trabéculas Cárneas**: Mais finas e numerosas que as do VD.
    - **Músculos Papilares**: Dois grandes músculos papilares (anterior e posterior), que se conectam às cúspides da valva mitral.
    - **Via de Saída (Vestíbulo Aórtico)**: Porção lisa que leva à valva aórtica.

![Anatomia interna das quatro câmaras cardíacas com destaque para as valvas e músculos papilares](https://s37942.pcdn.co/wp-content/uploads/2024/06/anatomia-do-coracao-1.webp)

### 2.3. Septos Cardíacos

- **Septo Interatrial**: Separa os átrios.
- **Septo Interventricular**: Separa os ventrículos. Possui duas porções:
    - **Porção Muscular**: Espessa, constitui a maior parte do septo.
    - **Porção Membranácea**: Fina e fibrosa, localizada na parte superior, próxima às valvas aórtica e tricúspide. É um local comum de **Comunicação Interventricular (CIV)**, a cardiopatia congênita mais frequente.
- **Septo Atrioventricular**: Pequena porção que separa o AD do VE.

### 2.4. Esqueleto Fibroso do Coração

Estrutura de tecido conjuntivo denso que serve a múltiplos propósitos:

- **Ponto de Fixação**: Fornece inserção para as valvas cardíacas e para o miocárdio atrial e ventricular.
- **Isolante Elétrico**: Separa eletricamente os átrios dos ventrículos, garantindo que o impulso elétrico passe exclusivamente através do sistema de condução (feixe de His).
- **Manutenção da Integridade Estrutural**: Impede a distorção dos óstios valvares durante o ciclo cardíaco.

É composto principalmente por quatro anéis fibrosos (circundando as quatro valvas) e os trígonos fibrosos direito e esquerdo, que os conectam.

### 2.5. Valvas Cardíacas

Estruturas que garantem o fluxo unidirecional do sangue através do coração, abrindo e fechando passivamente em resposta aos gradientes de pressão.

| Valva | Localização | Número de Cúspides/Folhetos | Características |
| :--- | :--- | :--- | :--- |
| **Tricúspide** | Entre AD e VD | 3 (anterior, posterior, septal) | Cúspides presas a cordas tendíneas e músculos papilares. |
| **Mitral (Bicúspide)** | Entre AE e VE | 2 (anterior e posterior) | Cúspides presas a cordas tendíneas e músculos papilares. |
| **Pulmonar** | Entre VD e Tronco Pulmonar | 3 (anterior, direita, esquerda) | Valva semilunar (em formato de "ninho de andorinha"). Não possui cordas tendíneas. |
| **Aórtica** | Entre VE e Aorta | 3 (posterior, direita, esquerda) | Valva semilunar. As cúspides direita e esquerda dão origem às artérias coronárias. |

![Valvas cardíacas em vista superior após remoção dos átrios, mostrando anéis fibrosos e cúspides](https://www.kenhub.com/thumbor/eu1mNAwt3EmWdJnVwTFVDuQ4l-w=/fit-in/800x1600/filters:watermark(/images/logo_url.png,-10,-10,0):background_color(FFFFFF):format(jpeg)/images/library/11394/heart-valves_portuguese-2.jpg)

## 3. Vascularização Cardíaca

### 3.1. Circulação Coronariana

O miocárdio é suprido por duas artérias principais que se originam da aorta ascendente, logo acima da valva aórtica: as **artérias coronárias direita (ACD) e esquerda (ACE)**.

#### 3.1.1. Artéria Coronária Esquerda (ACE)

- **Tronco da Coronária Esquerda**: Curto, passa entre a aurícula esquerda e o tronco pulmonar.
- **Bifurcação**: Divide-se em dois ramos principais:
    - **Ramo Interventricular Anterior (AIA)** ou **Artéria Descendente Anterior (ADA)**: Percorre o sulco interventricular anterior em direção ao ápice. Irriga a parede anterior e anterosseptal dos ventrículos e o ápice. É a artéria mais comumente ocluída no infarto agudo do miocárdio.
    - **Ramo Circunflexo (ACx)**: Segue pelo sulco coronário esquerdo, contornando a face pulmonar do coração. Irriga a parede lateral e posterior do AE e VE.

#### 3.1.2. Artéria Coronária Direita (ACD)

- **Trajeto**: Percorre o sulco coronário direito.
- **Ramos Principais**:
    - **Ramo Marginal Direito**: Irriga a parede lateral do VD.
    - **Ramo Interventricular Posterior (AIP)** ou **Artéria Descendente Posterior (ADP)**: Na maioria das pessoas, origina-se da ACD na **cruz do coração** (junção dos sulcos coronário e interventricular posterior). Percorre o sulco interventricular posterior. Irriga a parede inferior e o terço posterior do septo interventricular.

#### 3.1.3. Dominância Cardíaca

Refere-se a qual artéria coronária origina o ramo interventricular posterior (AIP).
- **Dominância Direita (~67%)**: AIP origina-se da ACD.
- **Dominância Esquerda (~15%)**: AIP origina-se do ramo circunflexo (ACx).
- **Codominância (~18%)**: Ramos da ACD e ACx contribuem para a formação da AIP.

### 3.2. Drenagem Venosa

O sangue venoso do miocárdio é coletado por veias que, em sua maioria, convergem para o **seio coronário**.
- **Seio Coronário**: Grande veia localizada na porção posterior do sulco coronário, que desemboca no átrio direito.
- **Principais Tributárias**:
    - **Veia Cardíaca Magna**: Acompanha a ADA e a ACx.
    - **Veia Cardíaca Média**: Acompanha a AIP.
    - **Veia Cardíaca Parva**: Acompanha a ACD.
- **Veias Cardíacas Anteriores**: Drenam diretamente no átrio direito.
- **Veias Mínimas (de Tebésio)**: Pequenas veias que drenam diretamente nas quatro câmaras cardíacas.

![Artérias coronárias e veias cardíacas na superfície do coração](https://anatomia-papel-e-caneta.com/wp-content/uploads/2023/07/coracao-5.webp)

## 4. Sistema de Condução Elétrica

Conjunto de células miocárdicas especializadas responsáveis por gerar e conduzir o impulso elétrico que coordena a contração cardíaca.

![Esquema do sistema de condução do coração](https://www.souenfermagem.com.br/wp-content/uploads/2023/04/Sistema-de-conducao-eletrica-do-coracao.webp)

| Componente | Localização | Função |
| :--- | :--- | :--- |
| **Nó Sinoatrial (SA)** ou **de Keith-Flack** | Junção da VCS com o AD (na crista terminal). | **Marcapasso natural** do coração. Inicia o impulso elétrico com uma frequência intrínseca de 60-100 bpm. |
| **Vias Internodais** | Fibras no átrio direito que conectam o nó SA ao nó AV. | Conduzem o impulso através dos átrios. |
| **Nó Atrioventricular (AV)** ou **de Aschoff-Tawara** | No septo interatrial, próximo ao óstio do seio coronário (Triângulo de Koch). | **Atrasa a condução do impulso** (em ~0,1s) para permitir que os átrios se contraiam completamente antes dos ventrículos. Atua como marcapasso secundário (40-60 bpm) se o nó SA falhar. |
| **Feixe Atrioventricular (Feixe de His)** | Continuação do nó AV, perfura o esqueleto fibroso. | Única via de condução elétrica entre átrios e ventrículos. |
| **Ramos Direito e Esquerdo** | O feixe de His se divide nos ramos direito e esquerdo, que descem pelo septo interventricular. | Conduzem o impulso para os ventrículos direito e esquerdo, respectivamente. O ramo esquerdo se subdivide em fascículos anterior e posterior. |
| **Fibras de Purkinje** | Rede terminal que se ramifica a partir dos ramos e penetra no miocárdio ventricular. | Distribuem rapidamente o impulso elétrico para as células musculares ventriculares, garantindo uma contração sincronizada e eficiente, do ápice para a base. |
""", '.', 'resumo_cardiologia.pdf'
)

