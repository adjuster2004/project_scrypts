import os
from pathlib import Path

def create_project_tree(root_dir, output_filename="project_structure.txt", ignore_dirs=None):
    """
    Генерирует структуру проекта в виде дерева и сохраняет в текстовый файл.
    """
    # Папки, которые мы не хотим включать в итоговую структуру
    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules', '.idea', '.vscode'}

    root_path = Path(root_dir)
    
    with open(output_filename, "w", encoding="utf-8") as f:
        # Записываем корневую папку
        f.write(f"{root_path.absolute().name}/\n")
        
        def write_tree(dir_path, prefix=""):
            try:
                # Получаем содержимое директории
                items = list(dir_path.iterdir())
            except PermissionError:
                return # Пропускаем папки, к которым нет доступа
            
            # Фильтруем ненужные папки и сортируем (сначала папки, потом файлы)
            items = [item for item in items if item.name not in ignore_dirs]
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            count = len(items)
            for i, item in enumerate(items):
                is_last = (i == count - 1)
                connector = "└── " if is_last else "├── "
                
                if item.is_dir():
                    f.write(f"{prefix}{connector}{item.name}/\n")
                    # Для вложенных элементов добавляем отступ
                    extension = "    " if is_last else "│   "
                    write_tree(item, prefix + extension)
                else:
                    # Игнорируем сам скрипт генерации и итоговый текстовый файл
                    if item.name not in ["generate_tree.py", output_filename]:
                        f.write(f"{prefix}{connector}{item.name}\n")

        write_tree(root_path)

if __name__ == "__main__":
    # Укажите путь к проекту ('.' означает текущую директорию)
    PROJECT_PATH = "." 
    OUTPUT_FILE = "project_structure.txt"
    
    create_project_tree(PROJECT_PATH, OUTPUT_FILE)
    print(f"✅ Структура проекта успешно сохранена в файл: {OUTPUT_FILE}")