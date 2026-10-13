import sqlite3


class TriangleDatabase:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side1 REAL NOT NULL,
                side2 REAL NOT NULL,
                side3 REAL NOT NULL,
                triangle_type TEXT,
                error_message TEXT,
                coordinates TEXT,
                PRIMARY KEY (side1, side2, side3)
            )
        """)
        self.conn.commit()

    def add_record(self, side1, side2, side3, triangle_type, error_message, coordinates):
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?, ?)",
            (float(side1), float(side2), float(side3),
             triangle_type, error_message, str(coordinates)),
        )
        self.conn.commit()

    def get_record(self, side1, side2, side3):
        cur = self.conn.execute(
            "SELECT * FROM triangles WHERE side1=? AND side2=? AND side3=?",
            (float(side1), float(side2), float(side3)),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def delete_record(self, side1, side2, side3):
        cur = self.conn.execute(
            "DELETE FROM triangles WHERE side1=? AND side2=? AND side3=?",
            (float(side1), float(side2), float(side3)),
        )
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()