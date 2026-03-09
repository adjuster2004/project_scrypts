import os

# Папки, которые мы не хотим показывать в структуре
IGNORE_DIRS = {'.git', '__pycache__', 'venv', 'env', 'node_modules', '.idea', '.vscode'}

def print_tree(directory, prefix=""):
    try:
        # Получаем список файлов и папок
        entries = os.listdir(directory)
    except PermissionError:
        print(prefix + "└── [Доступ запрещен]")
        return

    # Фильтруем скрытые/служебные папки
    entries = [e for e in entries if not (os.path.isdir(os.path.join(directory, e)) and e in IGNORE_DIRS)]
    
    # Сортируем: сначала папки, потом файлы (по алфавиту)
    entries.sort(key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x.lower()))
    
    count = len(entries)
    for i, entry in enumerate(entries):
        is_last = (i == count - 1)
        
        # Выбираем правильные символы для отрисовки веток
        connector = "└── " if is_last else "├── "
        print(prefix + connector + entry)
        
        path = os.path.join(directory, entry)
        
        # Если это папка, рекурсивно заходим в неё
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension)

if __name__ == "__main__":
    print("=== Генератор структуры проекта ===")
    project_path = input("Введите путь к папке (или нажмите Enter для текущей): ").strip()
    
    if not project_path:
        project_path = "."
        
    abs_path = os.path.abspath(project_path)
    if not os.path.exists(abs_path):
        print("Ошибка: Указанный путь не существует.")
    else:
        print(f"\n📁 Структура проекта: {abs_path}\n")
        print(os.path.basename(abs_path) + "/")
        print_tree(abs_path)