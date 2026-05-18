import sqlite3
import re
import trafilatura
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from litellm import completion
from config import KEYWORDS, LLM_MODEL, DB_PATH

def translate_to_english(text):
    """Translate text to Arabic using deep-translator."""
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='auto', target='ar').translate(text)
    except Exception:
        return text

def truncate_words(text, n=300):
    """Truncate text to n words."""
    words = text.split()
    return ' '.join(words[:n])

def scrape_article_text(url):
    """Extract article text using trafilatura."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            if text:
                return text[:5000]
        return ''
    except Exception as e:
        print(f"Scrape Error for {url}: {e}")
        return ''

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles 
                      (id INTEGER PRIMARY KEY, title TEXT, link TEXT, score INTEGER, summary TEXT, image_url TEXT)''')
    for col in ['summary', 'image_url']:
        try:
            cursor.execute(f"ALTER TABLE articles ADD COLUMN {col} TEXT")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()

def rule_based_prefilter(title, content):
    """Simple keyword check."""
    text = f"{title} {content}".lower()
    for kw in KEYWORDS:
        if kw.lower() in text:
            return True
    return False

KEYWORD_SCORES = {
    "real madrid": 3, "xabi alonso": 3, "vinicius": 2, "mbappe": 2,
    "bellingham": 2, "ancelotti": 2, "bernabeu": 2, "endrick": 2,
    "kroos": 2, "modric": 2, "ucl": 1, "champions league": 1,
    "la liga": 1, "transfer": 1, "final": 1, "goal": 1,
}

def keyword_score(title, content):
    """Score article based on keyword relevance (fallback when LLM unavailable)."""
    text = f"{title} {content}".lower()
    score = 5
    for kw, pts in KEYWORD_SCORES.items():
        if kw in text:
            score += pts
    return min(score, 10)

def get_llm_score(title, content):
    """Get importance score (1-10) using LLM, falls back to keyword scoring on quota errors."""
    prompt = f"""
    Evaluate the following football article. 
    Importance criteria: 80% Real Madrid/Xabi Alonso, 20% Global Football.
    Article Title: {title}
    Article Content: {content}
    Return ONLY a single integer score from 1 to 10.
    """
    try:
        response = completion(model=LLM_MODEL, messages=[{"role": "user", "content": prompt}])
        score = int(response.choices[0].message.content.strip())
        return score
    except Exception as e:
        # Fall back to keyword scoring if rate-limited or quota exceeded
        fallback = keyword_score(title, content)
        print(f"LLM Error (using fallback score {fallback}): {e}")
        return fallback

def extract_image(entry, url):
    """Extract image URL from RSS entry or fallback to page scraping."""
    for mc in entry.get('media_content', []):
        img = mc.get('url')
        if img:
            return img
    for mt in entry.get('media_thumbnail', []):
        img = mt.get('url')
        if img:
            return img
    for link in entry.get('links', []):
        if link.get('type', '').startswith('image') and 'enclosure' in link.get('rel', ''):
            return link.get('href')
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            img = trafilatura.extract_metadata(downloaded)
            if img and hasattr(img, 'image'):
                return img.image
    except Exception:
        pass
    return ''

def process_article(title, link, content, image_url=''):
    """Hybrid pipeline: Pre-filter -> Scrape -> Translate -> Truncate -> LLM Score -> Store."""
    if not rule_based_prefilter(title, content):
        return None
    
    score = get_llm_score(title, content)
    if score >= 6:
        scraped = scrape_article_text(link)
        full = scraped if len(scraped) > len(content) else content
        translated = translate_to_english(full[:5000])
        summary = truncate_words(translated, 300)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO articles (title, link, score, summary, image_url) VALUES (?, ?, ?, ?, ?)",
                       (title, link, score, summary, image_url))
        conn.commit()
        conn.close()
        return score
    return None
