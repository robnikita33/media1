import json
import os
import subprocess
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

# --- ТВОИ ДАННЫЕ ---
API_TOKEN = '8378905620:AAEfVeZSXtzDbPFBEaCEUo0ifXOX15eG3oY'
JSON_FILE = 'news.json' # У тебя на скрине файл называется news.json
UPLOAD_DIR = 'uploads/'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class EventState(StatesGroup):
    waiting_for_name = State()
    waiting_for_media = State()

@dp.message(Command("new_event"))
async def start_event(message: types.Message, state: FSMContext):
    await message.answer("Введите название мероприятия для сайта:")
    await state.set_state(EventState.waiting_for_name)

@dp.message(EventState.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await message.answer(f"Пришли фото или видео для '{message.text}':")
    await state.set_state(EventState.waiting_for_media)

@dp.message(EventState.waiting_for_media, F.photo | F.video)
async def handle_media(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event_name = data['event_name']
    
    if message.photo:
        file = message.photo[-1]
        ext = ".jpg"
        m_type = "Фото"
    else:
        file = message.video
        ext = ".mp4"
        m_type = "Видео"

    file_info = await bot.get_file(file.file_id)
    file_name = f"media_{file.file_id[:8]}{ext}"
    path = os.path.join(UPLOAD_DIR, file_name)
    
    await bot.download_file(file_info.file_path, path)

    # Запись в JSON
    new_entry = {"title": event_name, "type": m_type, "date": "2026", "img": path}
    
    with open(JSON_FILE, 'r+', encoding='utf-8') as f:
        items = json.load(f)
        items.append(new_entry)
        f.seek(0)
        json.dump(items, f, ensure_ascii=False, indent=4)

    await message.answer("♻️ Синхронизация с GitHub...")
    
    # АВТО-ОБНОВЛЕНИЕ GITHUB
    try:
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Добавлено: {event_name}"])
        subprocess.run(["git", "push"])
        await message.answer("✅ Сайт обновлен! Проверь: robnikita33.github.io/media1/")
    except:
        await message.answer("❌ Ошибка GitHub. Проверь терминал на Mac.")
    
    await state.clear()

async def main():
    if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())