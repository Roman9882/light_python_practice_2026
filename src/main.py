import sys
import os
from collections import defaultdict
def print_help():
    print("""

                      Утилита для анализа папок
                      


    Назначение:
        Рекурсивный обход папки с выводом содержимого и формированием
        отчёта со статистикой.

    Запуск:
        python main.py <путь_к_папке> [фильтр]

    Что делает:
        - Рекурсивно обходит все вложенные папки
        - Показывает структуру папок и файлов с размерами
        - Формирует отчёт: количество папок/файлов, общий размер
        - Статистика по расширениям файлов
        - Фильтрация файлов по расширению

    Результат:
        Отчет выводится в консоль после обхода папки.

    """)





def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ['--help', '-h', '/?', 'help']:
        print_help()
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Ошибка: не передан путь к папке")
        print("Фильтр (необязательный): .txt, .py, .jpg и т.д.")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not folder_path or folder_path.strip() == '':
        print("Ошибка: путь к папке не может быть пустым")
        sys.exit(1)

    if any(c in folder_path for c in ['*', '?', '"', '<', '>', '|']):
        print("Ошибка: путь содержит недопустимые символы")
        sys.exit(1)

    file_filter = None
    if len(sys.argv) >= 3:
        file_filter = sys.argv[2]
        if not file_filter or file_filter.strip() == '':
            print("Ошибка: фильтр не может быть пустым")
            sys.exit(1)
        if not file_filter.startswith('.'):
            file_filter = '.' + file_filter

    if not os.path.exists(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует")
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print(f"Ошибка: '{folder_path}' не является папкой")
        sys.exit(1)

    print(f"Программа успешно запущена")
    print(f"Работаем с папкой: {folder_path}")
    if file_filter:
        print(f"Фильтр: только файлы с расширением {file_filter}")

    print("\nСодержимое папки:")
    stats = {
        'total_folders': 0,
        'total_files': 0,
        'total_size': 0,
        'extensions': defaultdict(int),
        'extensions_size': defaultdict(int)
    }

    walk_directory(folder_path, 0, stats, file_filter)
    print_report(stats, file_filter)

def walk_directory(path, level, stats, file_filter=None):

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
            stats['total_folders'] += 1
            print(f"{indent}[Папка] {item}/")
            walk_directory(item_path, level + 1, stats, file_filter)
        else:
            size = os.path.getsize(item_path)
            show_file = True
            if file_filter:
                ext = os.path.splitext(item)[1].lower()
                if ext != file_filter:
                    show_file = False

            if show_file:
                stats['total_files'] += 1
                stats['total_size'] += size

                ext = os.path.splitext(item)[1].lower()
                stats['extensions'][ext] += 1
                stats['extensions_size'][ext] += size

            print(f"{indent}[Файл] {item} ({size} байт)")

def format_size(size):
    if size < 1024:
        return f"{size} байт"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} кб"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} мб"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f} гб"


def print_report(stats, file_filter=None):
    print("\nОтчет")
    print(f"\nОбщая статистика:")
    print(f"    Папок: {stats['total_folders']}")
    print(f"    Файлов: {stats['total_files']}")
    print(f"    Общий размер: {format_size(stats['total_size'])}")

    if file_filter:
        print(f"\nФильтр: {file_filter}")

    if stats['extensions']:
        print(f"\nСтатистика по расширениям:")
        sorted_extensions = sorted(stats['extensions'].items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_extensions:
            total_size = stats['extensions_size'][ext]
            print(f"   {ext if ext else '(без расширения)'}: {count} файл(ов), {format_size(total_size)}")

main()