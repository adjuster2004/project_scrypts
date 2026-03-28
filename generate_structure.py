import os
import sys
import re
from pathlib import Path

def detect_format(lines: list[str]) -> str:
    """Определяет формат файла по наличию символов псевдографики дерева."""
    for line in lines:
        if re.search(r'[│├└─]', line):
            return 'tree'
    return 'flat'

def process_flat_format(lines: list[str], base_path: Path):
    """Обрабатывает плоский список с путями и контентом (через |)."""
    print("⚙️ Режим парсинга: ПЛОСКИЙ СПИСОК (Paths + Content)\n")
    for line in lines:
        line = line.strip()
        # Игнорируем пустые строки и комментарии
        if not line or line.startswith("#"):
            continue

        parts = line.split("|", 1)
        item_path_str = parts[0].strip()
        content = parts[1].strip().replace("\\n", "\n") if len(parts) > 1 else ""

        full_path = base_path / item_path_str

        if item_path_str.endswith("/"):
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"[DIR]  {full_path}")
        else:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"[FILE] {full_path}")

def process_tree_format(lines: list[str], base_path: Path):
    """Обрабатывает древовидную структуру (вывод команды tree)."""
    print("⚙️ Режим парсинга: ДЕРЕВО (Tree format)\n")
    path_stack = {0: base_path}

    for line_num, line in enumerate(lines, 1):
        original_line = line.rstrip('\n')
        
        # Очистка от мусора и комментариев <--
        line_clean = re.sub(r'\\s*', '', original_line)
        if "<--" in line_clean:
            line_clean = line_clean.split("<--")[0]
        
        # Пропускаем пустые строки и комментарии #
        if not line_clean.strip() or line_clean.strip().startswith("#"):
            continue

        # Вычисляем уровень вложенности
        prefix_match = re.match(r'^[\s│├└─]*', line_clean)
        prefix = prefix_match.group(0) if prefix_match else ""
        depth = len(prefix) // 4
        
        name = line_clean[len(prefix):].strip()
        if not name:
            continue

        is_dir = name.endswith("/") or name.endswith("\\")
        clean_name = name.rstrip("/\\")
        
        parent_dir = path_stack.get(depth)
        if parent_dir is None:
            print(f"⚠️ Ошибка отступов на строке {line_num}. Пропускаем: {name}")
            continue

        full_path = parent_dir / clean_name

        if is_dir:
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"[DIR]  {full_path}")
            path_stack[depth + 1] = full_path
        else:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as file:
                pass 
            print(f"[FILE] {full_path}")

def create_project_structure(config_file: str, base_dir: str):
    base_path = Path(base_dir)
    structure_path = Path(config_file)

    if not structure_path.exists():
        print(f"❌ Ошибка: Файл '{structure_path}' не найден.")
        sys.exit(1)

    print(f"🚀 Читаем структуру из {structure_path.name}...")
    print(f"📁 Целевая директория: {base_path.absolute()}")

    with open(structure_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Автоопределение формата и запуск нужного обработчика
    file_format = detect_format(lines)
    
    if file_format == 'tree':
        process_tree_format(lines, base_path)
    else:
        process_flat_format(lines, base_path)

    print("\n✅ Структура успешно сгенерирована!")

if __name__ == "__main__":
    # Аргументы: 1 - файл со структурой, 2 - целевая папка (по умолчанию output)
    config_path_arg = sys.argv[1] if len(sys.argv) > 1 else "structure.txt"
    target_dir_arg = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    create_project_structure(config_path_arg, target_dir_arg)
