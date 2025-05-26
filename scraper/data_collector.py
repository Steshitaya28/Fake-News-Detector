import time
import schedule
import os
import csv
from boom_scraper import fetch_fake_news
from rss_feed_parser import fetch_real_news  # your existing functions

CSV_FILE = "all_news.csv"

def export_to_csv(news_list):
    existing_news = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_news.append(row)

    combined_news = existing_news + news_list

    seen = set()
    deduped_news = []
    for news in combined_news:
        # Normalize keys to handle any whitespace differences
        title = news.get("title", "").strip()
        source = news.get("source", "").strip()
        unique_key = (title, source)
        if unique_key not in seen:
            seen.add(unique_key)
            deduped_news.append(news)

    fieldnames = ["title", "content", "source", "label"]
    with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduped_news)

    print(f" Exported {len(deduped_news)} unique news articles to {CSV_FILE}")

def main():
    print("Fetching real news...")
    real_news = fetch_real_news()

    print("Fetching fake news...")
    fake_news = fetch_fake_news()

    print(f" Real news fetched: {len(real_news)}")
    print(f" Fake news fetched: {len(fake_news)}")

    all_news = real_news + fake_news

    # Insert into your DB if needed here (not shown)

    # Export combined, deduplicated news to CSV
    export_to_csv(all_news)

# Scheduler
if __name__ == "__main__":
    main()  # Runs once and exits
