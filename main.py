import logging
import math

logger = logging.getLogger(__name__)


def calculate_triangle(a, b, c):
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except (ValueError, TypeError):
        logger.error("Нечисловые данные")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0:
        logger.error("Стороны должны быть положительными")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a + b <= c or a + c <= b or b + c <= a:
        logger.warning("Треугольник не существует")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a == b == c:
        triangle_type = "равносторонний"
    elif a == b or a == c or b == c:
        triangle_type = "равнобедренный"
    else:
        triangle_type = "разносторонний"

    x = (a * a + b * b - c * c) / (2 * a)
    y = math.sqrt(max(0, b * b - x * x))

    scale = 90 / max(a, abs(x), abs(x + a), y)

    coordinates = [
        (5, 5),
        (round(5 + a * scale), 5),
        (round(5 + x * scale), round(5 + y * scale))
    ]

    logger.info(
        "Результат: %s, координаты: %s",
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

        logger.info("Входные данные: %r, %r, %r", a, b, c)

        triangle_type, coordinates = calculate_triangle(a, b, c)

        print(triangle_type)
        print(coordinates)

    except Exception:
        logger.exception("Ошибка выполнения")

    logger.info("Приложение завершено")


if __name__ == "__main__":
    main()