import feedparser

def fetch_fake_news():
    # Expanded list of RSS feeds for fake news / fact-check sources (Indian + Intl)
    rss_feeds = [
        "https://factly.in/feed/",
        "https://www.altnews.in/feed/",
        "https://www.snopes.com/feed/",
        "https://www.poynter.org/ifcn/feed/",           # Poynter (International Fact-Checking Network)
        "https://www.fullfact.org/feed/",               # Full Fact (UK)
        "https://www.boomlive.in/feed/",                # Boomlive (India)
        "https://www.afp.com/en/newsroom/fact-check/feed", # AFP Fact Check
        "https://www.reuters.com/feeds/fact-check.xml", # Reuters Fact Check
        "https://www.factcheck.org/feed/",               # FactCheck.org (US)
        # Add any other reliable fact-check RSS feeds here
    ]

    news_items = []
    seen_titles = set()  # To avoid duplicates

    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title.strip()
            if title in seen_titles:
                continue  # skip duplicates by title
            seen_titles.add(title)

            content = entry.get("summary", "") or entry.get("content", [{"value": ""}])[0]["value"]
            source = entry.link if "link" in entry else ""

            news = {
                "title": title,
                "content": content,
                "source": source,
                "label": "fake"  # Since these are fact-check/fake news sources
            }
            news_items.append(news)

    return news_items

if __name__ == "__main__":
    fake_news = fetch_fake_news()
    print(f"Fetched {len(fake_news)} fake news articles")
    for news in fake_news[:5]:
        print(f"Title: {news['title']}")
        print(f"Source: {news['source']}")
        print(f"Content snippet: {news['content'][:150]}...\n")
