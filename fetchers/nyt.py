import requests
from config import NYT_API_KEY
from translator import translate_titles

LISTS = [
    "combined-print-and-e-book-nonfiction",
    "advice-how-to-and-miscellaneous",
    "business-books",
]

def fetch():
    books = []
    seen = set()
    for list_name in LISTS:
        url = (
            f"https://api.nytimes.com/svc/books/v3/lists/current/{list_name}.json"
            f"?api-key={NYT_API_KEY}"
        )
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            data = res.json()["results"]
            genre = data["display_name"]
            for b in data["books"]:
                isbn = b.get("primary_isbn13", "")
                if isbn in seen:
                    continue
                seen.add(isbn)
                books.append({
                    "rank": b["rank"],
                    "title": b["title"],
                    "author": b["author"],
                    "genre": genre,
                    "isbn": isbn,
                    "source": "NYT",
                })
        except Exception:
            pass

    books = sorted(books, key=lambda x: x["rank"])

    titles = [b["title"] for b in books]
    ko_titles = translate_titles(titles)
    for b, kt in zip(books, ko_titles):
        b["ko_title"] = kt

    return books
