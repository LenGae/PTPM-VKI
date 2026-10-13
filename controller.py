from calculator import TriangleCalculator
from database import TriangleDatabase
from user_interface import IUserInterface
from notifier import INotifier


class Controller:
    def __init__(
        self,
        ui: IUserInterface,
        db: TriangleDatabase,
        notifier: INotifier,
        calculator: TriangleCalculator | None = None,
    ):
        self.ui = ui
        self.db = db
        self.notifier = notifier
        self.calculator = calculator or TriangleCalculator()

    def run(self) -> str:
        a, b, c = self.ui.get_input()

        record = self.db.get_record(a, b, c)

        if record is None:
            triangle_type, error, coordinates = self.calculator.determine_type(a, b, c)
            self.db.add_record(a, b, c, triangle_type, error, coordinates)

            if error:
                result = f"Ошибка: {error}. Тип: {triangle_type or 'не определён'}"
            else:
                result = f"Тип треугольника: {triangle_type}, координаты: {coordinates}"
        else:
            if record["error_message"]:
                result = (
                    f"Ошибка: {record['error_message']}. "
                    f"Тип: {record['triangle_type'] or 'не определён'}"
                )
            else:
                result = (
                    f"Тип треугольника: {record['triangle_type']}, "
                    f"координаты: {record['coordinates']}"
                )

        self.notifier.send(result)
        self.ui.show_result(result)

        return result