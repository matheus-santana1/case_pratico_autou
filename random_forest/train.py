import pandas as pd
import joblib
import string
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

nltk_data_dir = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path.append(nltk_data_dir)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("portuguese"))


def preprocess(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = [
        lemmatizer.lemmatize(word)
        for word in text.split()
        if word not in stop_words
    ]
    return " ".join(tokens)


if __name__ == '__main__':
    df = pd.read_csv("dataset.csv")

    df["tipo"] = df["tipo"].map({"produtivo": 1, "improdutivo": 2})

    df["mensagem"] = df["mensagem"].fillna("").apply(preprocess)

    X_train, X_test, y_train, y_test = train_test_split(
        df["mensagem"], df["tipo"], test_size=0.3, random_state=42
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000)),
        ("clf", RandomForestClassifier(n_estimators=200, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=["Improdutivo", "Produtivo"]))

    joblib.dump(pipeline, "modelo_random_forest.pkl")
    print("Modelo salvo em modelo_random_forest.pkl")

    mc = confusion_matrix(y_test, y_pred)
    print("Matriz de Confusão:\n", mc)

    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {acc:.2%}")
