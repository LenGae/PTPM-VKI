import os
import unittest

from src.database import DatabaseRepository
from src.parser import ForumParser


FIXTURE = os.path.join(
    os.path.dirname(__file__), "fixtures", "quotes_fixture.html"
)


class TestForumParser(unittest.TestCase):
    def setUp(self):
        self.parser = ForumParser()
        self.repo = DatabaseRepository(':memory:')

    def tearDown(self):
        self.repo.close()

    def test_parse_fixture_finds_items(self):
        posts = self.parser.parse_file(FIXTURE)
        self.assertGreater(len(posts), 0)

    def test_parse_fixture_ids_are_ints(self):
        for p in self.parser.parse_file(FIXTURE):
            self.assertIsInstance(p["id"], int)

    def test_parse_fixture_has_required_fields(self):
        for p in self.parser.parse_file(FIXTURE):
            self.assertIn("id", p)
            self.assertIn("name", p)
            self.assertIn("message", p)
            self.assertTrue(p["name"])
            self.assertTrue(p["message"])

    def test_save_to_db(self):
        posts = self.parser.parse_file(FIXTURE)
        saved = self.parser.save_to_db(posts, self.repo)
        self.assertEqual(saved, len(posts))

    def test_save_to_db_idempotent(self):
        posts = self.parser.parse_file(FIXTURE)
        self.parser.save_to_db(posts, self.repo)
        self.assertEqual(self.parser.save_to_db(posts, self.repo), 0)

    def test_headers_contain_user_agent(self):
        self.assertIn("User-Agent", self.parser.session.headers)

    def test_debug_show_db(self):
        posts = self.parser.parse_file(FIXTURE)
        self.parser.save_to_db(posts, self.repo)
        all_rows = self.repo.connection.execute("SELECT id, name, message FROM comments").fetchall()
        print("\n--- Содержимое БД ---")
        for row in all_rows:
            print(dict(row))
        print(f"Всего записей: {len(all_rows)}")


if __name__ == "__main__":
    unittest.main()