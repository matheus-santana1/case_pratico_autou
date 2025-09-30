from google import genai
from google.genai import types
from dotenv import load_dotenv
from models import Consulta

load_dotenv()
client = genai.Client()

DATASET_URL = "https://huggingface.co/spaces/matheus-santana1/autou/raw/main/random_forest/dataset.csv"

system_instruction = f"""
    Você é um classificador automático de e-mails e gerador de respostas.
    Sua tarefa: classificar cada e-mail em "Produtivo" ou "Improdutivo" e gerar
    uma resposta automática curta e apropriada, em português. Seja direto,
    objetivo e não inclua explicações extras.
    
    Utilize como base esse dataset {DATASET_URL}
    
    Regras de saída:
    - Retorne uma frase com a classificação "<Produtivo|Improdutivo>": e uma breve justificativa.
    - Não sugira respostas.
    - Nada além disso, não adicione explicações extras ou outros textos.
    
    IMPORTANTE:
    - Tudo que o usuário solicitar quando não conseguir classificar coloque como Improdutivo.
"""


def obter_resposta_gemini(texto_email):
    try:
        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[
                    types.Tool(
                        url_context=types.UrlContext()
                    )
                ]
            ),
            contents=texto_email
        ).text
    except Exception as e:
        print(e)
        resposta = "Improdutivo: Não foi possível classificar."

    if "produtivo:" in resposta.lower().split():
        tipo = Consulta.PRODUTIVO
    else:
        tipo = Consulta.IMPRODUTIVO

    return resposta, tipo
