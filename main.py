from models import *
from PyPDF2 import PdfReader
import streamlit as st
import pandas as pd
import plotly.express as px


def load_css(file_name: str):
    with open(file_name) as file_css:
        st.markdown(f"<style>{file_css.read()}</style>", unsafe_allow_html=True)


@st.dialog("Resposta")
def modal_resposta(informacao):
    st.markdown(
        f"""
        <div style="padding: 15px; border-radius: 10px; background-color: #f0f2f6; box-shadow: 0 2px 8px rgba(0,0,0,0.1)
        ;">
            <h4 style="color: #1f77b4; margin-bottom: 10px;">Classificador (Random Forest)</h4>
            <p style="font-size: 16px; color: #333;">{informacao.resposta_classificador}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div style="padding: 15px; border-radius: 10px; background-color: #fdf6f0; box-shadow: 0 2px 8px rgba(0,0,0,0.1)
        ; margin-top: 10px;">
            <h4 style="color: #ff7f0e; margin-bottom: 10px;">API (Google Gemini)</h4>
            <p style="font-size: 16px; color: #333;">{informacao.resposta_api}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


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
                '<div style="display: flex; justify-content: center;">──── ou ────</div>'
            )
            files = st.file_uploader('Arquivo(s) de e-mail:', type=['txt', 'pdf'], accept_multiple_files=True)
            submit = st.form_submit_button('Consultar')
            if submit:
                if text_input.strip():
                    info = Consulta.create(conteudo_email=text_input)
                    modal_resposta(info)
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

        tab1, tab2 = st.tabs(["Dados", "Gráficos"])

        if not dataframe.empty:
            with tab1:
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
                    Consulta.resposta_classificador.verbose_name: st.column_config.Column(width='medium',
                                                                                          disabled=True),
                    Consulta.resposta_api.verbose_name: st.column_config.Column(width='medium', disabled=True),
                    Consulta.data.verbose_name: st.column_config.DatetimeColumn(width='small', disabled=True,
                                                                                format="DD/MM/YYYY"),
                    'tipo_api': None,
                    'tipo_classificador': None,
                })

                if st.button("Remover selecionados"):
                    linhas_selecionadas = data_editor.index[data_editor["Remover"]].tolist()
                    ids_para_remover = ids.iloc[linhas_selecionadas].tolist()

                    if ids_para_remover:
                        Consulta.delete().where(Consulta.id.in_(ids_para_remover)).execute()
                        st.rerun()
                    else:
                        st.warning("Nenhum item selecionado.")

            with tab2:
                col1, col2 = st.columns(2, border=True)

                df = pd.DataFrame(list(Consulta.select().dicts()))
                mapa_tipos = {1: "Improdutivo", 2: "Produtivo"}
                df["tipo_classificador_nome"] = df["tipo_classificador"].map(mapa_tipos)
                df["tipo_api_nome"] = df["tipo_api"].map(mapa_tipos)

                contagem_api = df["tipo_api_nome"].value_counts().reset_index()
                contagem_api.columns = ["Tipo", "Quantidade"]

                contagem_classificador = df["tipo_classificador_nome"].value_counts().reset_index()
                contagem_classificador.columns = ["Tipo", "Quantidade"]

                fig_api = px.bar(contagem_api, x="Tipo", y="Quantidade",
                                 title="API (Google Gemini)",
                                 color="Tipo", text="Quantidade")

                fig_classificador = px.bar(contagem_classificador, x="Tipo", y="Quantidade",
                                           title="Classificador (Random Forest)",
                                           color="Tipo", text="Quantidade")

                with col1:
                    st.plotly_chart(fig_api, use_container_width=True)

                with col2:
                    st.plotly_chart(fig_classificador, use_container_width=True)
        else:
            st.info("Nenhuma consulta realizada.")
