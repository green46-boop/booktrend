import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9",
}


def _normalize(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    stopwords = {"the", "a", "an", "of", "in", "and", "to", "is"}
    words = [w for w in title.split() if w not in stopwords]
    return " ".join(words)


def get_crossover(country_books: dict) -> list:
    """2개국 이상 등장하는 도서 반환. country_books = {country_name: [books]}"""
    norm_map = {}  # normalized_title -> {country: original_title}
    for country, books in country_books.items():
        for book in books:
            key = _normalize(book["title"])
            if not key:
                continue
            if key not in norm_map:
                norm_map[key] = {"title": book["title"], "author": book.get("author", ""), "countries": {}}
            norm_map[key]["countries"][country] = book["rank"]

    crossovers = [
        {
            "title": v["title"],
            "author": v["author"],
            "countries": v["countries"],
            "count": len(v["countries"]),
        }
        for v in norm_map.values()
        if len(v["countries"]) >= 2
    ]
    return sorted(crossovers, key=lambda x: -x["count"])


def get_genre_stats(books: list) -> dict:
    """장르별 도서 수 집계. 장르 없는 책은 제외."""
    stats = {}
    for book in books:
        genre = book.get("genre", "").strip()
        if not genre:
            continue
        stats[genre] = stats.get(genre, 0) + 1
    return dict(sorted(stats.items(), key=lambda x: -x[1]))


def check_korean_pub(title: str) -> bool:
    """알라딘에서 한국어 번역판 존재 여부 확인."""
    try:
        url = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&SearchWord={quote(title)}&BranchType=1"
        res = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".ss_book_box")
        for item in items[:5]:
            cat = item.select_one(".tit_category")
            if cat and "[국내도서]" in cat.get_text():
                return True
        return False
    except Exception:
        return False


def get_unpublished_kr(foreign_books: list) -> list:
    """해외 베스트셀러 중 한국 미출간 도서 반환."""
    result = []
    for book in foreign_books:
        if not check_korean_pub(book["title"]):
            result.append(book)
    return result
