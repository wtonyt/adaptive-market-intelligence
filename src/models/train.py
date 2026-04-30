import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


def load_data():
    df = pd.read_parquet("data/gold/market_features.parquet")
    return df


def prepare_data(df):
    # Features we created
    features = ["return", "ma_5", "ma_10", "volatility_5"]

    X = df[features]
    y = df["target"]

    return X, y


def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))
    print("\nClassification Report:\n")
    print(classification_report(y_test, preds))


if __name__ == "__main__":
    df = load_data()

    X, y = prepare_data(df)

    # Simple split (later we’ll improve this)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = train_model(X_train, y_train)

    evaluate(model, X_test, y_test)
