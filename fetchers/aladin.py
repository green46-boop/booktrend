import requests
from bs4 import BeautifulSoup

URL = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&DisplayCount=20&SortOrder=1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}

def fetch():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        books = []
        items = soup.select(".ss_book_box")
        for i, item in enumerate(items[:20], 1):
            title_el = item.select_one(".bo3 a") or item.select_one("a.bo3")
            if not title_el:
                continue
            author_links = item.select('a[href*="AuthorSearch"]')
            author_str = ", ".join(a.get_text(strip=True) for a in author_links)
            books.append({
                "rank": i,
                "title": title_el.get_text(strip=True),
                "author": author_str,
                "genre": "",
                "isbn": "",
                "source": "알라딘",
            })
        return books
    except Exception:
        return []
