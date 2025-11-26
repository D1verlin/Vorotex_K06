import os
import subprocess
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item

# --- НАСТРОЙКИ ---
TOOL_NAME = "ch57x-keyboard-tool.exe"  # Имя программы-прошивальщика

# Список профилей: ("Название в меню", "имя_файла.yaml")
PROFILES = [
    ("Работа", "work.yaml"),
    ("Стрелки", "arrows.yaml"),
    ("Медиа", "media.yaml")
]
# -----------------

def create_image(color1, color2):
    # Генерируем иконку (квадрат)
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height), fill=color2)
    return image

def run_config(icon, config_file):
    # Путь к файлу
    current_dir = os.getcwd()
    tool_path = os.path.join(current_dir, TOOL_NAME)
    config_path = os.path.join(current_dir, config_file)

    if not os.path.exists(config_path):
        icon.notify(f"Файл не найден: {config_file}", "Ошибка")
        return

    # Команда для запуска
    cmd = [tool_path, "upload", config_path]
    
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    try:
        subprocess.run(cmd, startupinfo=startupinfo, check=True)
        icon.notify(f"Загружен профиль: {config_file}", "Успешно")
    except subprocess.CalledProcessError:
        icon.notify("Ошибка прошивки. Проверьте кабель.", "Ошибка")
    except Exception as e:
        icon.notify(str(e), "Ошибка")

def exit_action(icon, item):
    icon.stop()

# --- ИСПРАВЛЕННАЯ ЧАСТЬ ---
def make_action(filename):
    """
    Создает "обертку" для действия кнопки.
    Это решает проблему с ошибкой ValueError в Python 3.13
    """
    def action(icon, item):
        run_config(icon, filename)
    return action

def setup_menu():
    menu_items = []
    for name, filename in PROFILES:
        # Теперь мы вызываем make_action, чтобы создать правильную функцию
        menu_items.append(item(name, make_action(filename)))
    
    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(item('Выход', exit_action))
    
    return pystray.Menu(*menu_items)
# --------------------------

if __name__ == "__main__":
    # Рисуем иконку (Сине-черный квадрат)
    icon_img = create_image('blue', 'black')
    
    icon = pystray.Icon("VorotexSwitcher", icon_img, "Vorotex K06 Control", setup_menu())
    icon.run()