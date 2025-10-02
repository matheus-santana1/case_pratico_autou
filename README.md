# AutoU — Classificação e Resposta Automática de Emails

Este projeto implementa uma aplicação web que **classifica emails automaticamente** em duas categorias — **Produtivo**
ou **Improdutivo** — e gera **respostas automáticas sugeridas** com base no conteúdo identificado.

A solução combina técnicas de **aprendizado de máquina tradicional (Random Forest)** e **IA generativa (Google Gemini)
**, garantindo previsibilidade e robustez, além de respostas mais naturais e contextuais.

Deploy público no Hugging Face Spaces:
👉 [AutoU no Hugging Face](https://huggingface.co/spaces/matheus-santana1/autou)

---

## 🚀 Funcionalidades

* Upload de emails em **.txt** ou **.pdf** ou inserção direta de texto.
* Classificação automática em **Produtivo** ou **Improdutivo**.
* Sugestão de resposta automática adequada à categoria.
* Combinação de dois algoritmos de classificação:

    * **Random Forest** — modelo clássico de ML, treinado com exemplos rotulados.
    * **Google Gemini** — modelo de linguagem para interpretação do contexto e geração de respostas.
* Interface web simples, intuitiva e responsiva.

---

## 📂 Estrutura do Projeto

```
/
├── exemplos/               # Arquivos de exemplo para testes
├── random_forest/          # Scripts relacionados ao modelo Random Forest
├── .streamlit/             # Configurações de UI (Streamlit)
├── database.db             # Banco de dados SQLite (opcional, histórico)
├── genai.py                # Integração com Google Gemini
├── main.py                 # Ponto de entrada da aplicação (Streamlit app)
├── models.py               # Modelos e utilitários
├── styles.css              # Arquivo de estilos da interface
├── requirements.txt        # Dependências do projeto
└── README.md               
```

---

## 🛠 Como Executar Localmente

1. Clone este repositório:

   ```bash
   git clone https://github.com/matheus-santana1/case_pratico_autou.git
   cd case_pratico_autou
   ```

2. Crie um ambiente virtual e ative:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux / macOS
   # venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure sua chave de API do **Google Gemini** (ou outro modelo de IA generativa):

   ```bash
   export GEMINI_API_KEY="sua_chave_aqui"
   ```

5. Execute a aplicação:

   ```bash
   streamlit run main.py
   ```

6. Acesse em `http://localhost:8501`.

---

## 🧠 Estratégia de Classificação

1. **Pré-processamento do texto** — remoção de stop words, normalização e lematização.
2. **Random Forest** — realiza a primeira classificação baseada em padrões aprendidos.
3. **Google Gemini** — interpreta o contexto do email e sugere uma resposta adequada.
4. **Combinação dos resultados** — lógica que integra as saídas dos dois métodos, priorizando consistência e clareza
   para o usuário.

---

## 🧪 Exemplos de Uso

Na pasta `exemplos/`, você encontrará arquivos de teste:

* Emails de **solicitação de suporte** → classificados como **Produtivo**.
* Emails de **felicitações** → classificados como **Improdutivo**.

Cada email enviado retorna:

* **Categoria atribuída**
* **Sugestão de resposta automática**

---

## 🌐 Deploy no Hugging Face

A aplicação já está disponível online no Hugging Face Spaces:
👉 [AutoU no Hugging Face](https://matheus-santana1-autou.hf.space/)

---

## 🎥 Vídeo de Apresentação

👉 [Youtube](https://www.youtube.com/watch?v=fPlB4Mc5YG8)

---

## ⚠️ Limitações

* Emails muito longos ou com linguagem ambígua podem afetar a classificação.
* Dependência de limites de uso da API do Google Gemini.
* O modelo Random Forest depende da qualidade do dataset usado para treinamento.

**Possíveis melhorias futuras:**

* Retraining incremental com feedback do usuário.
* Interface mais avançada com histórico e edição de respostas.

---

## 👤 Autor

Desenvolvido por **Matheus Santana**
📧 Contato: [matheussantana2099@gmail.com](mailto:matheussantana2099@gmail.com)
🌐 [LinkedIn](https://www.linkedin.com/in/matheus-santana-159ab1246/) | [GitHub](https://github.com/matheus-santana1)

---