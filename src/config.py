import os

# RSS Configuration
RSS_FEEDS = [
    "https://www.espn.com/espn/rss/soccer/news",
    "https://www.skysports.com/rss/11661", # Real Madrid news
    "https://www.marca.com/rss/futbol/real-madrid.xml",
    "https://feeds.bbci.co.uk/sport/football/rss.xml",
    "https://www.theguardian.com/football/rss",
    "https://www.goal.com/feeds/en/news",
    "https://www.goal.com/feeds/en/la-liga",
    "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
    "https://www.marca.com/rss/futbol/la-liga.xml",
    "https://www.marca.com/rss/futbol/champions-league.xml",
    "https://feeds.feedburner.com/soccernewsfeed",
    "https://www.eyefootball.com/football_news.xml",
    "https://www.eyefootball.com/rss_news_transfers.xml",
    "https://www.football365.com/feed",
    "https://talksport.com/feed",
    "http://rss.cnn.com/rss/edition_sport.rss",
    "https://soccerlens.com/feed",
    "https://www.thesun.co.uk/sport/football/feed/",
    "https://www.dailymail.co.uk/sport/football/index.rss",
    "https://www.fourfourtwo.com/feed"
]

# Keywords for Pre-filtering
KEYWORDS = ["real madrid", "xabi alonso", "vinicius", "mbappe", "bellingham", "ancelotti", "kroos", "modric", "bernabeu", "endrick", "copa del rey", "supercopa", "la liga", "champions", "ucl", "uefa", "copa", "transfer"]

# Database Configuration
DB_PATH = "data/news.db"

# LLM Configuration
# Updated for Google Gemini
LLM_MODEL = "gemini/gemini-2.0-flash"
