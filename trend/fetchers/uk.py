import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.co.uk/gp/bestsellers/books/274081"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.9",
}

def fetch():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        books = []
        items = soup.select("#gridItemRoot")
        for i, item in enumerate(items[:20], 1):
            img = item.select_one("img")
            title = img.get("alt", "").strip() if img else ""
            if not title:
                continue
            author_el = item.select_one(".a-size-small a")
            books.append({
                "rank": i,
                "title": title,
                "author": author_el.get_text(strip=True) if author_el else "",
                "genre": "non-fiction",
                "isbn": "",
                "source": "Amazon UK",
            })
        return books
    except Exception:
        return []
