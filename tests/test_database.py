import sqlite3
import unittest

from src.database import DatabaseRepository, ValidationError


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repo = DatabaseRepository(':memory:')

    def tearDown(self):
        self.repo.close()

    def test_add_success(self):
        self.assertTrue(self.repo.add(1, "alice", "Hello"))
        rec = self.repo.get_by_id(1)
        self.assertEqual(rec["id"], 1)
        self.assertEqual(rec["name"], "alice")
        self.assertEqual(rec["message"], "Hello")

    def test_add_duplicate_id_raises(self):
        self.repo.add(1, "alice", "Hello")
        with self.assertRaises(sqlite3.IntegrityError):
            self.repo.add(1, "bob", "Duplicate")

    def test_add_invalid_name_too_long(self):
        with self.assertRaises(ValidationError):
            self.repo.add(1, "x" * 257, "msg")

    def test_add_invalid_message_too_long(self):
        with self.assertRaises(ValidationError):
            self.repo.add(1, "alice", "x" * 8097)

    def test_add_invalid_id_type(self):
        with self.assertRaises(ValidationError):
            self.repo.add("not-int", "alice", "msg")

    def test_get_by_id_existing(self):
        self.repo.add(1, "alice", "Hi")
        rec = self.repo.get_by_id(1)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["message"], "Hi")

    def test_get_by_id_missing_returns_none(self):
        self.assertIsNone(self.repo.get_by_id(999))

    def test_get_by_name_returns_all_user_posts(self):
        self.repo.add(1, "alice", "A1")
        self.repo.add(2, "alice", "A2")
        self.repo.add(3, "bob", "B1")
        posts = self.repo.get_by_name("alice")
        self.assertEqual(len(posts), 2)
        self.assertTrue(all(p["name"] == "alice" for p in posts))

    def test_get_by_name_empty(self):
        self.assertEqual(self.repo.get_by_name("nobody"), [])

    def test_get_by_name_invalid_type(self):
        with self.assertRaises(ValidationError):
            self.repo.get_by_name(123)

    def test_update_existing(self):
        self.repo.add(1, "alice", "old")
        self.assertTrue(self.repo.update(1, "new"))
        self.assertEqual(self.repo.get_by_id(1)["message"], "new")

    def test_update_missing_returns_false(self):
        self.assertFalse(self.repo.update(999, "new"))

    def test_update_too_long_message_raises(self):
        self.repo.add(1, "alice", "ok")
        with self.assertRaises(ValidationError):
            self.repo.update(1, "x" * 8097)

    def test_delete_existing(self):
        self.repo.add(1, "alice", "to delete")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_missing_returns_false(self):
        self.assertFalse(self.repo.delete(999))


if __name__ == "__main__":
    unittest.main()