import feedparser
import newspaper

# デフォルトのRSSフィード
RSS_FEEDS = [
    "https://www.world-nuclear-news.org/rss",
    "https://www.mining.com/tag/uranium/feed",
    "https://www.cameco.com/rss/news",
    "https://www.reuters.com/rssFeed/nuclear",
    "https://www.marketscreener.com/rss/uranium",
    "https://investingnews.com/category/daily/resource-investing/energy-investing/uranium-investing/feed/",
    "https://www.neimagazine.com/rss/news",
    "https://phys.org/rss-feed/tags/uranium",
    "https://globalnews.ca/tag/uranium/feed",
    "https://www.canalaska.com/feed/",
    "https://fissilematerials.org/blog/atom.xml"
]

def fetch_articles(rss_feeds=RSS_FEEDS, per_feed=3):
    """RSSから記事を取得して本文を抽出"""
    articles = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:per_feed]:
            content = extract_content(entry.link)
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "content": content or entry.get("summary", ""),
                "published_parsed": entry.published_parsed,
            })
    return articles

def extract_content(url):
    """newspaperで本文を抽出"""
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        if article.text.strip():
            return article.text
    except Exception as e:
        print(f"[ERROR] Failed to extract article from {url}: {e}")
    return None
