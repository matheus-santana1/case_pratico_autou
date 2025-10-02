from models import *
from PyPDF2 import PdfReader
import streamlit as st
import pandas as pd
import plotly.express as px
import html


def load_css(file_name: str):
    with open(file_name) as file_css:
        st.markdown(f"<style>{file_css.read()}</style>", unsafe_allow_html=True)


@st.dialog("Resposta")
def modal_resposta(informacao):
    st.markdown(f"**Conteúdo do e-mail:** {informacao.conteudo_email}")
    st.markdown(f"**Data da consulta:** {informacao.data:%d/%m/%Y às %H:%M}.")

    st.markdown(
        f"""
        <div class="classificador-style">
            <h4>Classificador (Random Forest)</h4>
            <p><b>{informacao.resposta_classificador}.</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    texto_original = html.escape(informacao.resposta_api)
    analise_gemini = texto_original.replace("\n", "<br>")
    analise_gemini = analise_gemini.replace("Improdutivo:", "<b>Improdutivo:</b>")
    analise_gemini = analise_gemini.replace("Produtivo:", "<b>Produtivo:</b>")

    resposta_final = None
    if "Resposta:" in analise_gemini:
        partes = analise_gemini.split("Resposta:", 1)
        analise_gemini = partes[0].strip()  # só até antes da resposta
        resposta_final = partes[1].strip()  # só a resposta, sem <b>

    st.markdown(
        f"""
        <div class="google-style" style="margin: 10px 0px 10px 0px;">
            <h4>API (Google Gemini)</h4>
            <p>{analise_gemini}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if resposta_final:
        st.markdown("**Resposta:**")
        st.code(resposta_final, wrap_lines=True, language="text")


if __name__ == '__main__':
    load_css("styles.css")
    if db.is_closed():
        db.connect()
    db.create_tables([Consulta])
    st.set_page_config(
        page_title="Case Prático AutoU",
        page_icon="📊",
        layout="wide"
    )
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
                            info = Consulta.create(conteudo_email=f.read().decode("utf-8"))
                        elif f.name.endswith(".pdf"):
                            reader = PdfReader(f)
                            texto_pdf = "\n".join([page.extract_text() for page in reader.pages])
                            info = Consulta.create(conteudo_email=texto_pdf)
                        if len(files) == 1:
                            modal_resposta(info)
                else:
                    st.error('É necessário preencher o conteúdo do e-mail ou enviar pelo menos um arquivo de e-mail.')
        dataframe = pd.DataFrame(list(Consulta.select().dicts()))

        tab1, tab2 = st.tabs(["Consultas", "Gráficos"])

        if not dataframe.empty:
            with tab1:
                ids = dataframe["id"].tolist()
                selecionados = []

                for idx, row in dataframe.iterrows():
                    consulta_id = row["id"]

                    with st.container():
                        cols = st.columns([0.05, 0.05, 0.9])

                        with cols[0]:
                            if st.button("🔍", key=f"ver_{consulta_id}"):
                                consulta = Consulta.get(Consulta.id == consulta_id)
                                modal_resposta(consulta)

                        with cols[1]:
                            if st.checkbox("Selecionar", key=f"chk_{consulta_id}", label_visibility="collapsed"):
                                selecionados.append(consulta_id)

                        with cols[2]:
                            conteudo_email = html.escape(row['conteudo_email']).replace("\n", "<br>")
                            st.markdown(
                                f"""
                                <div style="
                                    display: flex;
                                    width: 100%;
                                    gap: 1.5rem;
                                ">
                                    <div style="
                                        flex: 1;
                                        white-space: nowrap;
                                        overflow: hidden;
                                        text-overflow: ellipsis;
                                    ">
                                        {conteudo_email}
                                    </div>
                                    <div class="classificador-style classificador-row 
                                {"produtivo" if row['tipo_classificador'] == Consulta.PRODUTIVO else "improdutivo"}">
                                        {row['resposta_classificador']}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                if st.button("Remover selecionados"):
                    ids_protegidos = ids[:10]  # protege os 10 primeiros
                    ids_para_remover = [i for i in selecionados if i not in ids_protegidos]

                    if ids_para_remover:
                        Consulta.delete().where(Consulta.id.in_(ids_para_remover)).execute()
                        st.success(f"{len(ids_para_remover)} item(s) removido(s).")
                        st.rerun()
                    else:
                        st.warning("Nenhum item selecionado ou apenas itens protegidos.")

            with tab2:
                col1, col2 = st.columns(2, border=True)

                df = pd.DataFrame(list(Consulta.select().dicts()))
                mapa_tipos = {1: "Produtivo", 2: "Improdutivo"}
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
