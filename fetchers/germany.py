import requests
from bs4 import BeautifulSoup

URL = "https://www.spiegel.de/bestseller/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9",
}

def fetch():
    try:
        res = requests.get(URL, headers=HEADERS, timeout=10, allow_redirects=True)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        books = []

        rank_els = soup.find_all(
            "p",
            string=lambda t: t and t.strip().isdigit() and 1 <= int(t.strip()) <= 20
        )

        for r in rank_els[:20]:
            container = r.find_parent("div")
            for _ in range(5):
                parent = container.find_parent("div")
                if not parent:
                    break
                container = parent
                if len(container.get_text(strip=True)) > 80:
                    break

            title_el = container.find(
                "span",
                class_=lambda c: c and "lg:text-xl" in c and "font-bold" in c
            )
            author_els = [p for p in container.find_all("p") if not p.get("class") and p.get_text(strip=True)]
            title = title_el.get_text(strip=True) if title_el else ""
            author = author_els[0].get_text(strip=True) if author_els else ""
            if not title:
                continue
            books.append({
                "rank": int(r.get_text(strip=True)),
                "title": title,
                "author": author,
                "genre": "Sachbuch",
                "isbn": "",
                "source": "Spiegel",
            })

        return sorted(books, key=lambda x: x["rank"])
    except Exception:
        return []
