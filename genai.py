from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

system_instruction = """
    Você é um classificador automático de e-mails e gerador de respostas.
    Sua tarefa: classificar cada e-mail em "Produtivo" ou "Improdutivo" e gerar
    uma resposta automática curta e apropriada, em português. Seja direto,
    objetivo e não inclua explicações extras.
    
    Regras de saída:
    - Retorne uma frase com a classificação "<Produtivo|Improdutivo>": e uma breve justificativa.
    - Nada além disso, não adicione explicações extras ou outros textos.
"""


def obter_resposta_gemini(texto_email):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        ),
        contents=texto_email
    ).text
