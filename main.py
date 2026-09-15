import logging
import math
import sys
import os


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)

logger.info("Логгер успешно сконфигурирован")


def calculate_triangle(a, b, c):
    logger.debug(
        "Начало вычисления. Получены стороны: A=%r, B=%r, C=%r",
        a, b, c
    )

    try:
        a = float(a)
        b = float(b)
        c = float(c)

        logger.debug(
            "Строки успешно преобразованы в числа: A=%s, B=%s, C=%s",
            a, b, c
        )

    except (ValueError, TypeError):
        logger.error(
            "Нечисловые данные: A=%r, B=%r, C=%r",
            a, b, c
        )

        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logger.error(
            "Некорректные числовые данные. "
            "Все стороны должны быть положительными: A=%s, B=%s, C=%s",
            a, b, c
        )

        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a + b <= c or a + c <= b or b + c <= a:
        logger.warning(
            "Треугольник не существует. Стороны: A=%s, B=%s, C=%s",
            a, b, c
        )

        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        triangle_type = "равносторонний"
    elif a == b or a == c or b == c:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    logger.debug("Определён вид треугольника: %s", triangle_type)

    x = (a * a + b * b - c * c) / (2 * a)
    y = math.sqrt(max(0, b * b - x * x))

    logger.debug(
        "Рассчитаны исходные координаты: x=%s, y=%s",
        x, y
    )

    max_size = max(a, abs(x), abs(x + a), y)

    scale = 90 / max_size

    coordinates = [
        (5, 5),
        (round(5 + a * scale), 5),
        (round(5 + x * scale), round(5 + y * scale))
    ]

    logger.info(
        "Успешный расчёт. Тип: %s, координаты: %s",
        triangle_type,
        coordinates
    )

    return triangle_type, coordinates


def main():
    logger.info("Приложение запущено")

    try:
        a = input("Введите длину первой стороны: ")
        b = input("Введите длину второй стороны: ")
        c = input("Введите длину третьей стороны: ")

        logger.info(
            "Получены входные данные: A=%r, B=%r, C=%r",
            a, b, c
        )

        triangle_type, coordinates = calculate_triangle(a, b, c)

        print("Тип треугольника:", triangle_type)
        print("Координаты вершин:", coordinates)

        logger.info(
            "Результат выведен пользователю: тип=%s, координаты=%s",
            triangle_type,
            coordinates
        )

    except Exception:
        logger.exception("Произошла непредвиденная ошибка выполнения")

    logger.info("Приложение завершено")


if __name__ == "__main__":
    main()
