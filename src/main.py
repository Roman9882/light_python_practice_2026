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

    print("\nСодержимое папки:")
    walk_directory(folder_path, 0)


def walk_directory(path, level):

    items = os.listdir(path)
    folders = []
    files = []
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folders.append(item)
        else:
            files.append(item)

    folders.sort()
    files.sort()
    sorted_items = folders + files

    for item in sorted_items:
        item_path = os.path.join(path, item)
        indent = "    " * level

        if os.path.isdir(item_path):
            print(f"{indent}[Папка] {item}/")
            walk_directory(item_path, level + 1)
        else:
            size = os.path.getsize(item_path)
            print(f"{indent}[Файл] {item} ({size} байт)")

main()