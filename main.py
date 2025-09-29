from model import *
from PyPDF2 import PdfReader
import streamlit as st
import pandas as pd


def load_css(file_name: str):
    with open(file_name) as file_css:
        st.markdown(f"<style>{file_css.read()}</style>", unsafe_allow_html=True)


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    load_css("styles.css")
    if db.is_closed():
        db.connect()
    db.create_tables([Consulta])
    with st.container():
        with st.form(key='form', clear_on_submit=True):
            text_input = st.text_area('Conteúdo do e-mail:')
            st.html(
                '<div style="display: flex; justify-content: center;">──────────── ou ────────────</div>'
            )
            files = st.file_uploader('Arquivo(s) de e-mail:', type=['txt', 'pdf'], accept_multiple_files=True)
            submit = st.form_submit_button('Consultar')
            if submit:
                if text_input.strip():
                    Consulta.create(conteudo_email=text_input)
                elif files:
                    for f in files:
                        if f.name.endswith(".txt"):
                            Consulta.create(conteudo_email=f.read().decode("utf-8"))
                        elif f.name.endswith(".pdf"):
                            reader = PdfReader(f)
                            texto_pdf = "\n".join([page.extract_text() for page in reader.pages])
                            Consulta.create(conteudo_email=texto_pdf)
                else:
                    st.error('É necessário preencher o conteúdo do e-mail ou enviar pelo menos um arquivo de e-mail.')
        dataframe = pd.DataFrame(list(Consulta.select().dicts()))

        if not dataframe.empty:
            dataframe.rename(columns={'conteudo_email': Consulta.conteudo_email.verbose_name,
                                      'resposta_classificador': Consulta.resposta_classificador.verbose_name,
                                      'resposta_api': Consulta.resposta_api.verbose_name,
                                      'data': Consulta.data.verbose_name}, inplace=True)

            ids = dataframe["id"].copy()
            dataframe["Remover"] = False
            dataframe.drop(columns=["id"], inplace=True)

            data_editor = st.data_editor(dataframe, hide_index=True, column_config={
                "Remover": st.column_config.CheckboxColumn(
                    help="Marque para remover esta linha",
                    default=False,
                    width=10
                ),
                Consulta.conteudo_email.verbose_name: st.column_config.Column(width='medium', disabled=True),
                Consulta.resposta_classificador.verbose_name: st.column_config.Column(width='medium', disabled=True),
                Consulta.resposta_api.verbose_name: st.column_config.Column(width='medium', disabled=True),
                Consulta.data.verbose_name: st.column_config.DatetimeColumn(width='small', disabled=True,
                                                                            format="DD/MM/YYYY"),
            })

            if st.button("Remover selecionados"):
                linhas_selecionadas = data_editor.index[data_editor["Remover"]].tolist()
                ids_para_remover = ids.iloc[linhas_selecionadas].tolist()

                if ids_para_remover:
                    Consulta.delete().where(Consulta.id.in_(ids_para_remover)).execute()
                    st.rerun()
                else:
                    st.warning("Nenhum item selecionado para remover.")
        else:
            st.info("Nenhuma consulta realizada.")
