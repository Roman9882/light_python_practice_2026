import sys
import os


def main():
    if len(sys.argv) < 2:
        print("Ошибка: не передан путь к папке")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует")
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print(f"Ошибка: '{folder_path}' не является папкой")
        sys.exit(1)

    print(f"Программа успешно запущена")
    print(f"Работаем с папкой: {folder_path}")

main()