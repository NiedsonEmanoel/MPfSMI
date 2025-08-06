import logging
from google import genai
from google.genai import types
from typing import Optional
from utilities import load_file_content, build_config
import searchImage 
searchImage.chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_resume(
    transcricao: str,
    key_path: Optional[str] = "../../gemini.key",
    prompt_path: Optional[str] = "../Prompts/Resumo.txt",
    model_name: str = "gemini-2.5-pro"
) -> str:
    """
    Gera um resumo em Markdown a partir de uma transcrição, usando Gemini API.
    """
    try:
        # Carregar chave e prompt
        api_key = load_file_content(key_path, "chave da API Gemini")
        prompt_text = load_file_content(prompt_path, "prompt do resumo")

        # Inicializar cliente Gemini
        client = genai.Client(api_key=api_key)

        # Preparar entrada
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=transcricao)],
            )
        ]

        config = build_config(prompt_text)

        # Gerar conteúdo
        logger.info("Iniciando geração do resumo com Gemini...")
        markdown_chunks = []
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config,
        ):
            markdown_chunks.append(chunk.text)

        logger.info("Resumo gerado com sucesso.")
        Resumen = ''.join(markdown_chunks)
        # Preparar o Markdown para busca de imagens
        Resumen = searchImage.preparar_markdown_para_busca(Resumen)
        return Resumen
    
    except Exception as e:
        logger.exception("Erro ao gerar o resumo.")
        raise RuntimeError(f"Erro ao gerar o resumo: {e}")


# Execução direta para testes
if __name__ == "__main__":
    exemplo_transcricao = """
tecido epitelial formado células bem unidas si quer saber quais funções características assista vídeo gosta estudar vídeos sabe inscrevase canal curta vídeo tecido epitelial tecidos corpo humano formado células justapostas intimamente unidas umas outras através junções interselulares proteínas integrais membrana traduzindo ficam unidas estruturas parecidas velcros principal função tecido epitelial revestir superficie externa corpo cavidades corporais internas órgãos apresenta função secretora exemplo proteção revestimento pele cresção estômago cresção absorção intestino inpermeiabilização bechiga urinária estreita união células fazendo tecido epitelial barreira eficiente contra entrada agentes invasores perda líquidos corporais Além disso outras características células unidas forma bem organizada possui suprimento nervoso possui vasos sanguíneos alta capacidade renovação mitose regeneração nutrição oxigenação difusão lâmina basal quais tipos tecido epitelial acordo função existem dois tipos tecido epitelial revestimento glándular tecido epitelial revestimento epitelhos constituídos camadas células diferentes formas pouco quase nenhum fluido intersticial Porém todo epitelho situado sobre malha glícoproteca denominada lâmina basal função promover troca nutrientes tecido epitelial tecido conjuntivo vizinho acordo camadas celulares epitelhos podem classificados Epitelhos simples formados única camada células Epitelho estratificado formados camada células Epitelho pcou estratificado formados única camada células possui células alturas diferentes dando impressão estratificado tecido epitelial pele humana epidermi exemplo apresenta células bastante unidas sendo epitelho estratificado porque função pele evitar entrada corpos estranhos organismo agindo espécie barreira protetora Agora trata órgãos internos tecido epitelial cobre simples pois tecido pode tão espesso devido necessidade trocas substâncias Ah epitelhos classificados quanto forma células Epitelho pavimentoso possui células achatadas epitelho cúbico possui células forma cubo epitelho prismático células alongadas forma coluna epitelho transição forma original células cúbica ficam achatadas devido estiramento provocado dilatação órgão outro tipo tecido epitelial glandular onde células possuem mesmas características epitelho revestimento contrário raramente encontradas encamadas Portanto células unidas geralmente dispostas única camada epitelhos glándulares tecidos função secretora constituem órgãos especializados chamados glándulas maioria glándulas corpo humano formadas partir epitelho glándular podem dois tipos exócrinas endócrinas glándulas endócrinas ligação epitelho revestimento deixa existir células reorganizam folículos tireoide cordões adrenal tireoide ilhotas Langerhans glándulas exócrinas formadas duas partes parte secretora formada glándulas secreção duktor escritor composto células epiteliais revestimento lança secretões dentro cavidades internas glándulas salivares exterior corpo glándulas sudoríparas sebácias tecido epitelial Leia sobre link aqui descrição Continue estudando biologia gente Ficamos aqui próxima

"""
    resultado = generate_resume(exemplo_transcricao)
    print(resultado)
