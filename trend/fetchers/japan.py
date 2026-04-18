import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.co.jp/gp/bestsellers/books/466282"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9",
}

SKIP_KEYWORDS = ["アンアン", "anan", "週刊", "月刊", "号 No.", "ムック"]

def fetch():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        books = []
        rank = 1
        items = soup.select("#gridItemRoot")
        for item in items:
            img = item.select_one("img")
            title = img.get("alt", "").strip() if img else ""
            if not title:
                continue
            if any(kw in title for kw in SKIP_KEYWORDS):
                continue
            author_el = next(
                (s for s in item.find_all("span", class_="a-size-small")
                 if s.get_text(strip=True) and "%" not in s.get_text() and "Kindle" not in s.get_text() and not s.get_text(strip=True).isdigit()),
                None
            )
            books.append({
                "rank": rank,
                "title": title,
                "author": author_el.get_text(strip=True) if author_el else "",
                "genre": "ビジネス",
                "isbn": "",
                "source": "Amazon JP",
            })
            rank += 1
            if rank > 20:
                break
        return books
    except Exception:
        return []
