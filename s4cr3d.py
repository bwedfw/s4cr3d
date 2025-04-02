from telethon import TelegramClient, events
import os
import importlib.util
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


api_id = config["userbot"]["API_ID"]
api_hash = config["userbot"]["API_HASH"]

# Создаем клиента
client = TelegramClient('userbot', api_id, api_hash)

# Путь к папке с модулями
MODULES_DIR = "modules"

# Создаем папку для модулей, если её нет
os.makedirs(MODULES_DIR, exist_ok=True)

# Функция для загрузки модулей
def load_modules():
    for filename in os.listdir(MODULES_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Убираем расширение .py
            module_path = os.path.join(MODULES_DIR, filename)
            
            # Загружаем модуль
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Проверяем, что модуль содержит функцию setup
            if hasattr(module, "setup"):
                module.setup(client)  # Вызываем функцию setup
                print(f"Модуль {module_name} успешно загружен.")
            else:
                print(f"Модуль {module_name} не содержит функции setup.")

# Команда для загрузки нового модуля
@client.on(events.NewMessage(pattern=r'^\.dlmod\s+(https?://[^\s]+)$'))
async def download_module(event):
    url = event.pattern_match.group(1)  # Получаем URL модуля
    try:
        # Скачиваем файл
        response = await client.download_file(url)
        if not response:
            await event.edit("Ошибка: Не удалось скачать модуль.")
            return
        
        # Сохраняем файл в папку modules
        module_name = url.split("/")[-1]  # Имя файла из URL
        module_path = os.path.join(MODULES_DIR, module_name)
        with open(module_path, "wb") as f:
            f.write(response)
        
        # Загружаем модуль
        spec = importlib.util.spec_from_file_location(module_name[:-3], module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Проверяем, что модуль содержит функцию setup
        if hasattr(module, "setup"):
            module.setup(client)  # Вызываем функцию setup
            await event.edit(f"Модуль {module_name} успешно установлен!")
        else:
            await event.edit(f"Модуль {module_name} установлен, но не содержит функции setup.")
    except Exception as e:
        await event.edit(f"Ошибка при установке модуля: {str(e)}")

@client.on(events.NewMessage(pattern=r'^\.mdl'))
async def list_modules(event):
    try:
        # Сканируем папку modules
        modules = [f for f in os.listdir(MODULES_DIR) if f.endswith(".py") and not f.startswith("__")]
        
        if not modules:
            await event.reply("Нет доступных модулей.")
            return
        
        # Формируем список модулей
        module_list = "\n".join(modules)
        await event.reply(f"Список модулей:\n```\n{module_list}\n```")
    except Exception as e:
        await event.reply(f"Ошибка при получении списка модулей: {str(e)}")


@client.on(events.NewMessage(pattern=r'^\.dlmod\s+(https?://[^\s]+)$'))
async def download_module(event):
    url = event.pattern_match.group(1)  # Получаем URL модуля
    try:
        # Скачиваем файл
        response = requests.get(url)
        if response.status_code != 200:
            await event.edit("Ошибка: Не удалось скачать файл.")
            return
        
        # Извлекаем имя файла из URL
        filename = url.split("/")[-1]
        file_path = os.path.join(MODULES_DIR, filename)
        
        # Сохраняем файл в папку modules
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        await event.edit(f"Модуль {filename} успешно загружен.")
    except Exception as e:
        await event.edit(f"Ошибка при скачивании модуля: {str(e)}")



@client.on(events.NewMessage(pattern=r'^\.help'))
async def help(event):
    await client.send_message(event.chat_id, f"command ```.dlmod http://example.com/ ``` - скачивание файла с интернета\n command ```.help``` - показать это окно \n command ```.mdl``` - показать загруженные модули\n ```.reload``` - обновить модули\n подробнее: https://telegra.ph/s4cr3d-04-02")
# Команда для перезагрузки всех модулей
@client.on(events.NewMessage(pattern=r'^\.reload$'))
async def reload_modules(event):
    load_modules()
    await event.edit("Все модули перезагружены. ✅")

# Загружаем модули при старте
load_modules()

# Запуск клиента
print("Юзербот запущен...")
client.start()
client.run_until_disconnected()
