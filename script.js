/**
 * Скрипт для динамической подгрузки материалов Медиацентра Гимназии 261.
 * Поддерживает автоматическое распознавание фото и видео.
 */

async function renderGallery() {
    const gallery = document.getElementById('gallery');
    
    // Показываем индикатор загрузки, пока ждем файл
    gallery.innerHTML = '<p style="text-align: center; color: #86868b;">Загрузка последних событий...</p>';

    try {
        // Загружаем JSON-файл, который обновляет твой Python-бот
        // Добавляем параметр для предотвращения кэширования браузером
        const response = await fetch('events.json?v=' + new Date().getTime());
        
        if (!response.ok) {
            throw new Error('Файл данных не найден');
        }

        const eventData = await response.json();

        // Очищаем галерею перед выводом
        gallery.innerHTML = ''; 

        if (eventData.length === 0) {
            gallery.innerHTML = '<p style="text-align: center; color: #86868b;">Здесь пока пусто. Отправь что-нибудь боту!</p>';
            return;
        }

        // Выводим в обратном порядке (самые свежие новости будут первыми)
        eventData.reverse().forEach(item => {
            
            // Определяем, какой HTML использовать для медиа
            let mediaHtml = '';
            
            // Если тип "Видео" — создаем тег видео с автовоспроизведением при наведении
            if (item.type === 'Видео') {
                mediaHtml = `
                    <video 
                        src="${item.img}" 
                        class="card-img" 
                        muted 
                        loop 
                        playsinline
                        onmouseover="this.play()" 
                        onmouseout="this.pause(); this.currentTime = 0;">
                    </video>`;
            } else {
                // Иначе — обычная картинка
                mediaHtml = `<div class="card-img" style="background-image: url('${item.img}')"></div>`;
            }

            // Формируем полную карточку в стиле Apple
            const card = `
                <div class="card fade-in">
                    <div class="media-container">
                        ${mediaHtml}
                        <span class="type-tag">${item.type}</span>
                    </div>
                    <div class="card-content">
                        <p class="card-date">${item.date}</p>
                        <h3>${item.title}</h3>
                    </div>
                </div>
            `;
            
            gallery.innerHTML += card;
        });

    } catch (err) {
        console.error("Ошибка загрузки данных:", err);
        gallery.innerHTML = `
            <div style="text-align: center; padding: 20px;">
                <p style="color: #ff453a;">Не удалось загрузить материалы</p>
                <small style="color: #86868b;">Убедись, что бот создал файл events.json</small>
            </div>
        `;
    }
}

// Запускаем функцию сразу после полной загрузки страницы
document.addEventListener('DOMContentLoaded', renderGallery);