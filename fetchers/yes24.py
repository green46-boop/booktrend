import requests
from bs4 import BeautifulSoup

URL = "https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber=1&pageSize=24"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

def fetch():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser", from_encoding="euc-kr")
        books = []
        items = soup.select(".itemUnit")
        for i, item in enumerate(items[:20], 1):
            title_el = item.select_one(".info_name a")
            author_el = item.select_one(".info_auth")
            if not title_el:
                continue
            books.append({
                "rank": i,
                "title": title_el.get_text(strip=True),
                "author": author_el.get_text(strip=True) if author_el else "",
                "genre": "",
                "isbn": "",
                "source": "Yes24",
            })
        return books
    except Exception:
        return []
