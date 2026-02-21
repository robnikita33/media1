async function renderGallery() {
    const gallery = document.getElementById('gallery');
    
    try {
        // Указываем news.json (как на твоем скрине)
        const response = await fetch('news.json?v=' + Date.now());
        const data = await response.json();

        gallery.innerHTML = ''; 

        data.reverse().forEach(item => {
            const media = item.type === 'Видео' 
                ? `<video src="${item.img}" class="card-img" muted loop onmouseover="this.play()" onmouseout="this.pause()"></video>`
                : `<div class="card-img" style="background-image: url('${item.img}')"></div>`;

            gallery.innerHTML += `
                <div class="card">
                    <div class="media-container">
                        ${media}
                        <span class="type-tag">${item.type}</span>
                    </div>
                    <div class="card-content">
                        <h3>${item.title}</h3>
                        <p>${item.date}</p>
                    </div>
                </div>`;
        });
    } catch (e) {
        console.log("Ждем данных от бота...");
    }
}
document.addEventListener('DOMContentLoaded', renderGallery);