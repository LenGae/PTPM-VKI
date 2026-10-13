from abc import ABC, abstractmethod


class IUserInterface(ABC):
    @abstractmethod
    def get_input(self) -> tuple[str, str, str]:
        ...

    @abstractmethod
    def show_result(self, result: str) -> None:
        ...


class ConsoleUserInterface(IUserInterface):
    def get_input(self) -> tuple[str, str, str]:
        a = input("Введите длину первой стороны: ")
        b = input("Введите длину второй стороны: ")
        c = input("Введите длину третьей стороны: ")
        return a, b, c

    def show_result(self, result: str) -> None:
        print(result)