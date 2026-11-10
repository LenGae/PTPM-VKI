import hashlib
import sqlite3
from typing import List, Dict, Optional

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

    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = 10):
        self.headers = headers or self.DEFAULT_HEADERS
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch(self, url: str) -> str:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        return response.text

    def parse_html(self, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "lxml")
        items: List[Dict[str, str]] = []

        for block in soup.find_all("div", class_="quote"):
            author_el = block.find("small", class_="author")
            text_el = block.find("span", class_="text")
            if author_el is None or text_el is None:
                continue

            author = author_el.get_text(strip=True)
            message = text_el.decode_contents().strip()

            items.append({
                "id": self._stable_id(author, message),
                "name": author,
                "message": message,
            })
        return items

    def parse_page(self, url: str) -> List[Dict[str, str]]:
        return self.parse_html(self.fetch(url))

    def parse_file(self, filepath: str) -> List[Dict[str, str]]:
        with open(filepath, "r", encoding="utf-8") as f:
            return self.parse_html(f.read())

    @staticmethod
    def _stable_id(author: str, message: str) -> int:
        digest = hashlib.md5(f"{author}::{message}".encode("utf-8")).hexdigest()
        return int(digest[:12], 16)

    def save_to_db(self, parsed_data: List[Dict[str, str]], repository) -> int:
        saved = 0
        for item in parsed_data:
            try:
                repository.add(item["id"], item["name"], item["message"])
                saved += 1
            except sqlite3.IntegrityError:
                continue
        return saved