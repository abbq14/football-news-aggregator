# Project Map: Automated Football News Aggregator

## TECH_STACK
- **Language:** Python 3.12+
- **Framework:** Streamlit 1.30+ (UI)
- **RSS Parser:** `feedparser`
- **Web Scraper:** `trafilatura`
- **AI/LLM Interface:** `litellm`
- **Translation:** `deep-translator`
- **Database:** `sqlite3` (lightweight, file-based)

## SYSTEM_FLOW
1. **Fetch:** On manual "Refresh News" click, `feedparser` ingests raw RSS feed items (no background scheduler; Streamlit Cloud spins down when idle). Page loads instantly from the existing database without blocking on fetch.
2. **Rule-Based Pre-filter:** Regex/String check to retain only articles containing Real Madrid or Xabi Alonso related keywords (80% target). General football terms removed to reduce noise.
3. **LLM Scoring:** Surviving articles are passed to the LLM (via `litellm`) for a relevance score (1-10). Falls back to keyword scoring on quota errors. Keyword weights biased heavily toward Real Madrid/Xabi Alonso (4-3 range) over general football (1).
4. **Scrape & Translate:** Full article text is scraped from the URL via `trafilatura`, then translated to Arabic via `deep-translator` and truncated to ~300 words.
5. **Storage:** Only articles with a score >= 6 are stored in the SQLite database (title, link UNIQUE, score, summary ~300 words, image_url). Duplicate links are silently skipped via `INSERT OR IGNORE`.
6. **Display:** Streamlit UI queries the database and renders each article in a dark-themed card layout with:
   - Gradient title + subtitle
   - Score badge (pill-shaped, orange gradient)
    - Image (400px, col1) + Arabic summary (20px RTL, col2)
   - Styled "Read More →" link
   - Custom CSS (dark background `#0d1117`, card surface `#161b22`, accent `#f5a623`)
