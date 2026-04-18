import requests
from bs4 import BeautifulSoup

URL = "https://www.goodreads.com/shelf/show/non-fiction"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        books = []
        items = soup.select(".elementList")
        for i, item in enumerate(items[:20], 1):
            title_el = item.select_one(".bookTitle")
            author_el = item.select_one(".authorName")
            rating_el = item.select_one(".minirating")
            if not title_el:
                continue
            books.append({
                "rank": i,
                "title": title_el.get_text(strip=True),
                "author": author_el.get_text(strip=True) if author_el else "",
                "genre": "non-fiction",
                "isbn": "",
                "source": "Goodreads",
                "rating": rating_el.get_text(strip=True) if rating_el else "",
            })
        return books
    except Exception:
        return []
