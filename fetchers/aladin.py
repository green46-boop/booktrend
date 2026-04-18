import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

CATEGORIES = {
    "170":   "경제경영",
    "656":   "자기계발",
    "74":    "인문학",
    "75":    "역사",
    "76":    "사회과학",
    "77":    "자연과학",
    "1366":  "에세이",
    "55889": "건강/취미",
}

def _fetch_category(cid, genre, limit=10):
    url = (
        f"https://www.aladin.co.kr/shop/common/wbest.aspx"
        f"?BestType=Bestseller&BranchType=1&CID={cid}&DisplayCount={limit}&SortOrder=1"
    )
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        books = []
        for i, item in enumerate(soup.select(".ss_book_box")[:limit], 1):
            title_el = item.select_one("a.bo3")
            if not title_el:
                continue
            author_links = item.select('a[href*="AuthorSearch"]')
            author_str = ", ".join(a.get_text(strip=True) for a in author_links)
            books.append({
                "rank": i,
                "title": title_el.get_text(strip=True),
                "author": author_str,
                "genre": genre,
                "isbn": "",
                "source": "알라딘",
            })
        return books
    except Exception:
        return []

def fetch():
    seen = set()
    all_books = []
    for cid, genre in CATEGORIES.items():
        for book in _fetch_category(cid, genre, limit=5):
            key = book["title"]
            if key not in seen:
                seen.add(key)
                all_books.append(book)

    for i, book in enumerate(all_books, 1):
        book["rank"] = i
    return all_books
