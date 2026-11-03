class Converter:
    """Конвертер вещественных чисел по заданному алгоритму."""

    @staticmethod
    def do(x: float) -> int:
        """
        Принимает вещественное число x и возвращает целое число по алгоритму:
        - x >= 100.7        -> 1000
        - 0 < x < 100.7     -> int(x)
        - x == 0.0           -> ValueError
        - -30.4 <= x < 0     -> int(x) - 5
        - x <= -30.5         -> -2000
        """
        if x >= 100.7:
            return 1000
        elif x > 0:
            return int(x)
        elif x == 0.0:
            raise ValueError("Значение x не может быть равно нулю")
        elif x >= -30.4:
            return int(x) - 5
        else:
            return -2000
