import os
import sys

import requests


URL = "http://quotes.toscrape.com/"
OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tests", "fixtures", "quotes_fixture.html",
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}


def main() -> int:
    r = requests.get(URL, headers=HEADERS, timeout=20)
    print(f"Статус: {r.status_code}, {len(r.text)} символов")
    r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(r.text)

    print(f"Сохранено: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())