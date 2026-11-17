import sqlite3

import requests
from bs4 import BeautifulSoup


class ForumParser:
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    }

    def __init__(self, headers=None, timeout=10):
        self.headers = headers or self.DEFAULT_HEADERS
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch(self, url):
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        return response.text

    def parse_html(self, html):
        soup = BeautifulSoup(html, "lxml")
        items = []

        for idx, block in enumerate(soup.find_all("div", class_="quote"), start=1):
            author_el = block.find("small", class_="author")
            text_el = block.find("span", class_="text")
            if author_el is None or text_el is None:
                continue

            items.append({
                "id": idx,
                "name": author_el.get_text(strip=True),
                "message": text_el.decode_contents().strip(),
            })
        return items

    def parse_page(self, url):
        return self.parse_html(self.fetch(url))

    def parse_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return self.parse_html(f.read())

    def save_to_db(self, parsed_data, repository):
        saved = 0
        for item in parsed_data:
            try:
                repository.add(item["id"], item["name"], item["message"])
                saved += 1
            except sqlite3.IntegrityError:
                continue
        return saved