import pandas as pd
import sqlite3
import os

def load_kaggle_data_to_db(db_path="news_data.db", true_csv="True.csv", fake_csv="Fake.csv"):
    # Check if files exist
    if not os.path.exists(true_csv) or not os.path.exists(fake_csv):
        print("True.csv or Fake.csv not found. Please make sure the files are in the same directory.")
        return

    # Load Kaggle data
    real_df = pd.read_csv(true_csv)
    fake_df = pd.read_csv(fake_csv)

    # Add labels
    real_df["label"] = "real"
    fake_df["label"] = "fake"

    # Combine
    combined_df = pd.concat([real_df, fake_df], ignore_index=True)

    # Combine title and text into content field
    combined_df["content"] = combined_df["title"].fillna('') + ". " + combined_df["text"].fillna('')
    combined_df = combined_df[["title", "content", "label"]]

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            label TEXT CHECK(label IN ('real', 'fake'))
        );
    """)

    # Insert data
    for _, row in combined_df.iterrows():
        cursor.execute(
            "INSERT INTO news (title, content, label) VALUES (?, ?, ?)",
            (row["title"], row["content"], row["label"])
        )

    conn.commit()
    conn.close()

    print(f"Inserted {len(combined_df)} records into {db_path}.")

# Uncomment below to run independently
if __name__ == "__main__":
    load_kaggle_data_to_db()
