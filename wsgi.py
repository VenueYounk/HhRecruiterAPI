import sys
from main import app

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Обработка переданных аргументов командной строки
        arg1 = sys.argv[1]
        # Пример использования аргументов:
        app.config["scan"] = arg1
    app.config["JSON_AS_ASCII"] = False
    app.run()
