from flask import Flask, render_template, request
import sqlite3
import joblib
import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

MODEL_PATH = "fake_news_model.pkl"
DB_PATH = "news_data.db"

# Load model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None
    print("Model file not found. Please train and save the model first.")

def get_db_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT label FROM news", conn)
    conn.close()
    return df

def plot_label_distribution():
    df = get_db_data()
    counts = df['label'].value_counts()
    plt.figure(figsize=(5,4))
    counts.plot(kind='bar', color=['#0a74da', '#1ecbe1'])
    plt.title("News Label Distribution")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_b64

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form["text"]

    if not model:
        return "Model not loaded. Train the model first."

    prediction = model.predict([text])[0]
    confidence = max(model.predict_proba([text])[0]) * 100

    # Generate distribution chart
    dist_chart = plot_label_distribution()

    # Word count
    word_count = len(text.split())

    # Show prediction with confidence, word count, and distribution chart
    return render_template(
        "index.html",
        prediction=prediction.capitalize(),
        confidence=f"{confidence:.2f}",
        input_text=text,
        dist_chart=dist_chart,
        word_count=word_count
    )


if __name__ == "__main__":
    app.run(debug=True)
