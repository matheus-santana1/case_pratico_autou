from random_forest.train import preprocess
import joblib
from models import Consulta

modelo = joblib.load("modelo_random_forest.pkl")


def obter_resposta_random_forest(texto_email):
    texto_proc = preprocess(texto_email)
    pred = modelo.predict([texto_proc])[0]
    proba = modelo.predict_proba([texto_proc])[0]  # [p_improdutivo, p_produtivo]

    if pred == 1:
        resposta = f"Produtivo (certeza: {proba[1]:.2%})"
        tipo = Consulta.PRODUTIVO
    else:
        resposta = f"Improdutivo (certeza: {proba[0]:.2%})"
        tipo = Consulta.IMPRODUTIVO

    return resposta, tipo
