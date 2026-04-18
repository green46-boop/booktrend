import urllib.request
import json

API_KEY = "LJ4LMP52cxrS5ZQxBwe8S1OPEewkvuF1ATnvW87GJjWPkCmF"

LISTS = [
    "combined-print-and-e-book-nonfiction",
    "advice-how-to-and-miscellaneous",
    "business-books",
]

def fetch_top10(list_name):
    url = f"https://api.nytimes.com/svc/books/v3/lists/current/{list_name}.json?api-key={API_KEY}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data["results"]["books"][:10]

for list_name in LISTS:
    books = fetch_top10(list_name)
    print(f"\n=== NYT 베스트셀러: {list_name} ===\n")
    for book in books:
        print(f"{book['rank']:>2}위  {book['title']}  —  {book['author']}")

print()
