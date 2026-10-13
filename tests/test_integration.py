import unittest
from unittest.mock import MagicMock

from controller import Controller
from database import TriangleDatabase
from user_interface import IUserInterface
from notifier import INotifier

class TestControllerIntegration(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(":memory:")
        self.ui = MagicMock(spec=IUserInterface)
        self.notifier = MagicMock(spec=INotifier)
        self.notifier.send.return_value = True

        self.controller = Controller(ui=self.ui, db=self.db, notifier=self.notifier)

    def tearDown(self):
        self.db.close()

    def test_new_record_calculated_and_saved(self):
        self.ui.get_input.return_value = ("3", "3", "3")

        result = self.controller.run()

        self.assertIn("равносторонний", result)
        rec = self.db.get_record(3, 3, 3)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["triangle_type"], "равносторонний")
        self.assertIsNone(rec["error_message"])
        self.notifier.send.assert_called_once()

    def test_existing_record_taken_from_db(self):
        self.db.add_record(3, 4, 5, "разносторонний", None, "[(5, 5), (95, 5), (5, 95)]")

        self.ui.get_input.return_value = ("3", "4", "5")
        result = self.controller.run()

        self.assertIn("разносторонний", result)
        sent_message = self.notifier.send.call_args[0][0]
        self.assertIn("[(5, 5), (95, 5), (5, 95)]", sent_message)

    def test_error_record_saved_and_reported(self):
        self.ui.get_input.return_value = ("1", "2", "10")

        result = self.controller.run()

        self.assertIn("Ошибка", result)
        rec = self.db.get_record(1, 2, 10)
        self.assertIsNotNone(rec)
        self.assertIsNotNone(rec["error_message"])
        self.assertEqual(rec["triangle_type"], "не треугольник")
        self.notifier.send.assert_called_once()

    def test_second_call_uses_db_cache(self):
        self.ui.get_input.return_value = ("5", "5", "6")

        first = self.controller.run()
        second = self.controller.run()

        self.assertEqual(first, second)
        self.assertEqual(self.notifier.send.call_count, 2)
        rec = self.db.get_record(5, 5, 6)
        self.assertEqual(rec["triangle_type"], "равнобедренный")

    def test_notifier_failure_does_not_corrupt_db(self):
        self.notifier.send.side_effect = ConnectionError("server down")
        self.ui.get_input.return_value = ("6", "6", "6")

        with self.assertRaises(ConnectionError):
            self.controller.run()

        rec = self.db.get_record(6, 6, 6)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["triangle_type"], "равносторонний")