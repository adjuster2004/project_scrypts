import os
from pathlib import Path

def create_project_structure():
    base_path = Path("apps/client")

    # Список директорий для создания
    directories = [
        "src/app",
        "src/pages",
        "src/features/email/components",
        "src/features/calendar/components",
        "src/features/server-filters/components",
        "src/shared",
    ]

    # Словарь файлов и их стартового контента (комментариев)
    files = {
        "index.html": "\n",
        "vite.config.ts": "// Конфиг сборщика\n",
        "Dockerfile": "# Сборка Nginx образа для порта 443\n",
        "src/main.tsx": "// Рендер приложения\n",
        "src/pages/InboxPage.tsx": "// Страница входящих писем\n",
        "src/pages/CalendarPage.tsx": "// Страница календаря (наш фокус!)\n",
        "src/pages/SettingsPage.tsx": "// Настройки пользователя\n",
        "src/features/email/store.ts": "// Состояние (выбранные письма, кэш)\n",
        "src/features/calendar/utils.ts": "// Парсер iCal/ICS\n",
        "src/features/server-filters/api.ts": "// Отправка JSON-правил на бэкенд HopeDB\n",
    }

    print(f"Создаем структуру в {base_path.absolute()}...")

    # 1. Создаем директории
    for dir_path in directories:
        full_dir_path = base_path / dir_path
        full_dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Создана папка: {full_dir_path}")

    # 2. Создаем файлы
    for file_path, content in files.items():
        full_file_path = base_path / file_path
        # Создаем родительские папки, если их вдруг нет (хотя мы их создали выше)
        full_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Записываем контент в файл
        with open(full_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Создан файл:   {full_file_path}")

    print("\n✅ Структура успешно сгенерирована!")

if __name__ == "__main__":
    create_project_structure()