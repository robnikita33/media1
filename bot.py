# Обработка фото
@dp.message(EventState.waiting_for_photo, F.photo)
async def handle_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    
    file_name = f"img_{photo.file_id[:10]}.jpg"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    await bot.download_file(file_info.file_path, file_path)

    await save_to_json(data['event_name'], "Фотоотчет", file_path)
    await message.answer(f"📸 Фото для '{data['event_name']}' сохранено! Нажми /done для публикации.")

# Обработка видео
@dp.message(EventState.waiting_for_photo, F.video)
async def handle_video(message: types.Message, state: FSMContext):
    data = await state.get_data()
    video = message.video
    file_info = await bot.get_file(video.file_id)
    
    file_name = f"vid_{video.file_id[:10]}.mp4"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    await bot.download_file(file_info.file_path, file_path)

    await save_to_json(data['event_name'], "Видео", file_path)
    await message.answer(f"🎥 Видео для '{data['event_name']}' загружено! Нажми /done для публикации.")

# Вспомогательная функция для записи (чтобы не дублировать код)
async def save_to_json(name, media_type, path):
    new_entry = {
        "title": name,
        "type": media_type,
        "date": "Февраль 2026", 
        "img": path # Для видео JS подставит этот же путь в тег <video>
    }
    with open(JSON_FILE, 'r+', encoding='utf-8') as f:
        feeds = json.load(f)
        feeds.append(new_entry)
        f.seek(0)
        json.dump(feeds, f, ensure_ascii=False, indent=4)