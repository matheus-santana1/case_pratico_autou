import datetime
from peewee import *
from genai import obter_resposta_gemini

DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)


class Consulta(Model):
    conteudo_email = TextField(verbose_name='Conteúdo do e-mail')
    resposta_classificador = TextField(verbose_name='Classificador')
    resposta_api = TextField(verbose_name='API')
    data = DateTimeField(verbose_name='Data da consulta', default=datetime.datetime.now)

    class Meta:
        database = db

    @classmethod
    def create(cls, **kwargs):
        conteudo_email = kwargs.get('conteudo_email')
        kwargs.setdefault("resposta_classificador", "teste")
        kwargs.setdefault("resposta_api", obter_resposta_gemini(conteudo_email))
        return super().create(**kwargs)
