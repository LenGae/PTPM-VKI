from abc import ABC, abstractmethod


class INotifier(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        ...


class EmailNotifier(INotifier):
    def __init__(self):
        self.sent_messages: list[str] = []

    def send(self, message: str) -> bool:
        print(f"[EmailServer] Отправлено: {message}")
        self.sent_messages.append(message)
        return True