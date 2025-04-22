import requests
import json
import pandas as pd
import re
import os
import genanki

def gerar_flashcards(texto_base: str, titulo: str, pasta_destino):
    """
    Gera um deck de flashcards do Anki (.apkg) com base em um resumo médico.
    
    Parâmetros:
    - texto_base: conteúdo que será transformado em flashcards.
    - titulo: nome do deck e base para o nome do arquivo gerado.
    
    Saída:
    - Cria um arquivo .apkg com os flashcards, salvo no diretório atual.
    - Retorna o texto gerado com perguntas e respostas.
    """
    prompt = f"""A seguir, fornecerei um resumo de conteúdo médico. Sua tarefa é transformá-lo em **flashcards de alta qualidade para Anki**, com base nos seguintes critérios:

🎯 Objetivos:
- Clareza e objetividade (sem enrolação).
- Linguagem técnica adequada à medicina.
- Ênfase em raciocínio clínico, fisiopatologia, sinais-chave e condutas.
- Estrutura padronizada no formato pergunta e resposta curta.
- Organização por tópicos, caso o conteúdo envolva múltiplos subtemas.
- Inclusão de questões ao longo dos flashcards, sempre que fizer sentido.

📌 Exemplos de boas perguntas:
- "Qual é a tríade clássica da rubéola congênita?"
- "Como o CMV afeta o sistema nervoso central do feto?"
- "Qual o mecanismo fisiopatológico da insuficiência aórtica?"
- "Quais os principais achados no ECG da hipercalemia?"

✅ Formato da resposta:
Retorne a resposta **em formato padronizado**, sem ser no formato JSON, me mande estruturado pergunta/resposta como no exemplo abaixo:

      "pergunta": "Qual estrutura do coração inicia o impulso elétrico?",
      "resposta": "O nó sinoatrial (SA), localizado no átrio direito."

Segue o material do assunto que você usará como base e se sinta à vontade para complementar de forma que ajude no aprendizado médico:
{texto_base}
"""

    deck_id = abs(hash(titulo)) % (10**10)  # Gera um ID baseado no título
    model_id = 'enemaster'  # Modelo fixo

    my_deck = genanki.Deck(deck_id, titulo)

    my_model = genanki.Model(
        model_id,
        'Modelo Padrão',
        fields=[{'name': 'Pergunta'}, {'name': 'Resposta'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '{{Pergunta}}',
            'afmt': '{{Resposta}}',
        }],
    )

    # Lê a chave da API do arquivo gemini.key
    with open("gemini.key", "r") as file:
        API_KEY = file.read().strip()

    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        try:
            result = response.json()
            output_text = result['candidates'][0]['content']['parts'][0]['text']

            questions = re.findall(r'"pergunta": "(.*?)",\s*"resposta": "(.*?)"', output_text)
            df = pd.DataFrame(questions, columns=["pergunta", "resposta"])

            for _, row in df.iterrows():
                my_deck.add_note(genanki.Note(
                    model=my_model,
                    fields=[row['pergunta'], row['resposta']]
                ))

            nome_arquivo = f"{titulo.lower().replace(' ', '_')}.apkg"
            caminho = os.path.join(pasta_destino, nome_arquivo)
            my_deck.write_to_file(caminho)

            print(f"Deck '{titulo}' salvo como {caminho}.")
            return output_text

        except (KeyError, json.JSONDecodeError) as e:
            print("Erro ao processar a resposta:")
            print(response.text)
            raise e
    else:
        raise Exception(f"Erro na requisição: {response.status_code}\n{response.text}")

# Resumo de Fisiologia Digestória fornecido
resumo_fisiologia_digestoria = """
📍 1. Funções básicas do sistema digestório
- **Motilidade**: movimentação do conteúdo ao longo do trato gastrointestinal (TGI).
- **Secreção**: enzimas, muco, ácido e bicarbonato.
- **Digestão**: quebra de macromoléculas (carboidratos, proteínas e lipídios).
- **Absorção**: transporte de nutrientes, água e eletrólitos para o sangue/linfa.
- **Excreção**: eliminação de substâncias não absorvidas e resíduos.

📍 2. Controle neural e hormonal
- **Sistema nervoso entérico**: plexo mioentérico (Auerbach) e submucoso (Meissner).
- **Controle autônomo**: parassimpático (estimula digestão) e simpático (inibe).
- **Principais hormônios gastrointestinais**:
  - **Gastrina**: estimula secreção de HCl no estômago.
  - **Secretina**: estimula secreção de bicarbonato no pâncreas.
  - **Colecistocinina (CCK)**: libera enzimas pancreáticas e contrai vesícula biliar.
  - **GIP/GLP-1**: estimulam liberação de insulina (efeito incretina).

📍 3. Digestão e absorção por segmentos
🟡 **Boca**: Início da digestão de amido com amilase salivar. Função da mastigação e deglutição.

🔴 **Estômago**:
- Pepsina (ativa em pH ácido) inicia digestão de proteínas.
- Produção de HCl pelas células parietais.
- Secreção de fator intrínseco (absorção de B12 no íleo).
- Motilidade gera o quimo (conteúdo semi-líquido).

🟢 **Intestino delgado**: Local principal de digestão e absorção.
- Enzimas pancreáticas: amilase, lipase, tripsina, quimotripsina.
- Bile emulsifica gorduras.
- Absorção via microvilosidades (bordadura em escova).

🔵 **Intestino grosso**: Absorção de água e eletrólitos.
- Formação e armazenamento das fezes.
- Produção de vitaminas (K, B12, etc) por microbiota.

📍 4. Fases da digestão
- **Fase cefálica**: estímulo neural antes da alimentação (visão, cheiro, pensamento).
- **Fase gástrica**: distensão do estômago → secreção gástrica.
- **Fase intestinal**: controle da entrada do quimo no duodeno e secreção intestinal.
"""

gerar_flashcards(texto_base=resumo_fisiologia_digestoria, titulo='fisio', pasta_destino='')