import json
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

LIST_URL = "https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber=1&pageSize=20"
DETAIL_BASE = "https://www.yes24.com/product/goods/{}"


def _get_genre(goods_no):
    try:
        res = requests.get(DETAIL_BASE.format(goods_no), headers=HEADERS, timeout=8)
        soup = BeautifulSoup(res.content, "html.parser", from_encoding="euc-kr")
        for script in soup.find_all("script", type="application/ld+json"):
            data = json.loads(script.string)
            genres = data.get("genre", [])
            if genres:
                return genres[0] if isinstance(genres, list) else genres
    except Exception:
        pass
    return ""


def fetch():
    try:
        res = requests.get(LIST_URL, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser", from_encoding="euc-kr")
        books = []
        for i, item in enumerate(soup.select(".itemUnit")[:20], 1):
            title_el = item.select_one(".info_name a")
            author_el = item.select_one(".info_auth")
            link_el = item.select_one("a.lnk_img")
            if not title_el or not link_el:
                continue
            goods_no = link_el["href"].split("/")[-1]
            genre = _get_genre(goods_no)
            books.append({
                "rank": i,
                "title": title_el.get_text(strip=True),
                "author": author_el.get_text(strip=True) if author_el else "",
                "genre": genre,
                "isbn": "",
                "source": "Yes24",
            })
        return books
    except Exception:
        return []
