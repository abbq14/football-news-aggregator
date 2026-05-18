import streamlit as st
import feedparser
import sqlite3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from processor import process_article, init_db, extract_image
from config import RSS_FEEDS, DB_PATH

init_db()

def fetch_and_process():
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception:
            continue
        for entry in feed.entries:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM articles WHERE link = ?", (entry.link,))
            if not cursor.fetchone():
                img = extract_image(entry, entry.link)
                process_article(entry.title, entry.link, getattr(entry, 'description', ''), img)
            conn.close()

st.markdown("""
<style>
    .stApp { background: #0d1117; color: #e6edf3; }
    .stButton>button {
        background: linear-gradient(135deg, #f5a623, #e87d1e);
        color: #fff; border: none; border-radius: 8px;
        padding: 0.5rem 1.8rem; font-weight: 600;
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(245,166,35,0.4);
    }
    h1 {
        background: linear-gradient(135deg, #f5a623, #f7c948);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; letter-spacing: -0.5px; margin-bottom: 0.25rem;
    }
    .subtitle { color: #8b949e; font-size: 0.95rem; margin-bottom: 2rem; }
    .article-card {
        background: #161b22; border: 1px solid #30363d;
        border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .article-card h3 { color: #f0f6fc; margin: 0 0 0.5rem 0; }
    .article-card h3 a { color: #f0f6fc; text-decoration: none; }
    .article-card h3 a:hover { color: #f5a623; }
    .score-badge {
        display: inline-block; background: linear-gradient(135deg, #f5a623, #e87d1e);
        color: #fff; font-weight: 700; font-size: 0.8rem;
        padding: 0.2rem 0.7rem; border-radius: 20px; margin-bottom: 1rem;
    }
    .read-more {
        display: inline-block; margin-top: 0.75rem;
        color: #f5a623; font-weight: 600; text-decoration: none;
        border-bottom: 1px solid transparent; transition: border-color 0.15s;
    }
    .read-more:hover { border-bottom-color: #f5a623; }
</style>
""", unsafe_allow_html=True)

st.title("Real Madrid News Aggregator")
st.markdown("<p class='subtitle'>Automated football news — curated, translated, scored</p>", unsafe_allow_html=True)

if st.button("Refresh News"):
    with st.spinner("Fetching latest news..."):
        fetch_and_process()
    st.rerun()

conn = sqlite3.connect(DB_PATH)
articles = conn.execute("SELECT title, link, score, summary, image_url FROM articles ORDER BY id DESC").fetchall()
conn.close()

for title, link, score, summary, image_url in articles:
    st.markdown(f"""
<div class='article-card'>
    <h3><a href="{link}" target="_blank">{title}</a></h3>
    <span class='score-badge'>{score}/10</span>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    if image_url:
        col1.image(image_url, width=200)
    if summary:
        col2.markdown(f"<div style='font-size:20px; line-height:1.8; direction:rtl; text-align:right;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown(f"<a class='read-more' href='{link}' target='_blank'>Read More →</a>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
