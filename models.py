import datetime
from peewee import *

DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)


class Consulta(Model):
    PRODUTIVO = 1
    IMPRODUTIVO = 2

    conteudo_email = TextField(verbose_name='Conteúdo do e-mail')
    resposta_classificador = TextField(verbose_name='Classificador (Random Forest)')
    resposta_api = TextField(verbose_name='API (Google Gemini)')
    tipo_classificador = IntegerField(choices=[PRODUTIVO, IMPRODUTIVO])
    tipo_api = IntegerField(choices=[PRODUTIVO, IMPRODUTIVO])
    data = DateTimeField(verbose_name='Data da consulta', default=datetime.datetime.now)

    class Meta:
        database = db

    @classmethod
    def create(cls, **kwargs):
        from genai import obter_resposta_gemini
        from random_forest.api import obter_resposta_random_forest

        conteudo_email = kwargs.get('conteudo_email')
        resposta_classificador, tipo_classificador = obter_resposta_random_forest(conteudo_email)
        resposta_api, tipo_api = obter_resposta_gemini(conteudo_email)
        kwargs.setdefault("resposta_classificador", resposta_classificador)
        kwargs.setdefault("resposta_api", resposta_api)
        kwargs.setdefault("tipo_classificador", tipo_classificador)
        kwargs.setdefault("tipo_api", tipo_api)
        return super().create(**kwargs)
