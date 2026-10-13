from controller import Controller
from database import TriangleDatabase
from user_interface import ConsoleUserInterface
from notifier import EmailNotifier


def main():
    db = TriangleDatabase("triangles.db")
    ui = ConsoleUserInterface()
    notifier = EmailNotifier()

    controller = Controller(ui=ui, db=db, notifier=notifier)

    try:
        controller.run()
    finally:
        db.close()


if __name__ == "__main__":
    main()