import sqlite3
from typing import Optional, List, Dict, Any


class ValidationError(Exception):
    pass


class DatabaseRepository:
    MAX_NAME_LEN = 256
    MAX_MESSAGE_LEN = 8096

    def __init__(self, db_path: str = ':memory:'):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)

    @classmethod
    def _validate_name(cls, username: str) -> None:
        if not isinstance(username, str):
            raise ValidationError("name должен быть строкой")
        if not username or len(username) > cls.MAX_NAME_LEN:
            raise ValidationError(
                f"name должен быть непустым и не длиннее {cls.MAX_NAME_LEN} символов"
            )

    @classmethod
    def _validate_message(cls, message: str) -> None:
        if not isinstance(message, str):
            raise ValidationError("message должен быть строкой")
        if not message or len(message) > cls.MAX_MESSAGE_LEN:
            raise ValidationError(
                f"message должен быть непустым и не длиннее {cls.MAX_MESSAGE_LEN} символов"
            )

    @staticmethod
    def _validate_id(comment_id: int) -> None:
        if not isinstance(comment_id, int) or isinstance(comment_id, bool):
            raise ValidationError("id должен быть целым числом")

    def add(self, comment_id: int, username: str, message: str) -> bool:
        self._validate_id(comment_id)
        self._validate_name(username)
        self._validate_message(message)
        with self.connection:
            self.connection.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
        return True

    def get_by_id(self, comment_id: int) -> Optional[Dict[str, Any]]:
        self._validate_id(comment_id)
        cursor = self.connection.execute(
            "SELECT id, name, message FROM comments WHERE id = ?", (comment_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str) -> List[Dict[str, Any]]:
        self._validate_name(username)
        cursor = self.connection.execute(
            "SELECT id, name, message FROM comments WHERE name = ? ORDER BY id",
            (username,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def update(self, comment_id: int, new_message: str) -> bool:
        self._validate_id(comment_id)
        self._validate_message(new_message)
        with self.connection:
            cursor = self.connection.execute(
                "UPDATE comments SET message = ? WHERE id = ?",
                (new_message, comment_id),
            )
        return cursor.rowcount > 0

    def delete(self, comment_id: int) -> bool:
        self._validate_id(comment_id)
        with self.connection:
            cursor = self.connection.execute(
                "DELETE FROM comments WHERE id = ?", (comment_id,)
            )
        return cursor.rowcount > 0

    def close(self) -> None:
        self.connection.close()