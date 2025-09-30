import pandas as pd
import joblib
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

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
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

    df = pd.read_csv("random_forest/dataset.csv")

    df["tipo"] = df["tipo"].map({"produtivo": 1, "improdutivo": 0})

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
