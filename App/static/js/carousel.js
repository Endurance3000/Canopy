document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('carouselContainer');
    const cards = document.querySelectorAll('.carousel-card');
    const leftBtn = document.getElementById('scrollLeft');
    const rightBtn = document.getElementById('scrollRight');
    const progressBar = document.getElementById('scrollProgressBar');

    if (!container || cards.length === 0) return;

    // Scroll button clicks
    const scrollAmount = 320;

    if (leftBtn && rightBtn) {
        leftBtn.addEventListener('click', () => {
            container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });

        rightBtn.addEventListener('click', () => {
            container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
    }

    // Mouse Drag to Scroll
    let isDown = false;
    let startX;
    let scrollLeftPos;

    container.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - container.offsetLeft;
        scrollLeftPos = container.scrollLeft;
    });

    container.addEventListener('mouseleave', () => { isDown = false; });
    container.addEventListener('mouseup', () => { isDown = false; });

    container.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - container.offsetLeft;
        const walk = (x - startX) * 1.5; // Drag speed multiplier
        container.scrollLeft = scrollLeftPos - walk;
    });

    // Active Card Focus & Progress Bar
    const updateCarouselState = () => {
        const containerCenter = container.getBoundingClientRect().left + container.offsetWidth / 2;
        let minDistance = Infinity;
        let activeCard = null;

        cards.forEach(card => {
            const cardCenter = card.getBoundingClientRect().left + card.offsetWidth / 2;
            const distance = Math.abs(containerCenter - cardCenter);

            if (distance < minDistance) {
                minDistance = distance;
                activeCard = card;
            }
        });

        cards.forEach(card => card.classList.remove('active'));
        if (activeCard) {
            activeCard.classList.add('active');
        }

        if (progressBar) {
            const maxScroll = container.scrollWidth - container.clientWidth;
            const scrollPercent = maxScroll > 0 ? (container.scrollLeft / maxScroll) : 0;
            progressBar.style.transform = `translateX(${scrollPercent * 200}%)`;
        }
    };

    container.addEventListener('scroll', updateCarouselState);
    window.addEventListener('resize', updateCarouselState);
    
    setTimeout(updateCarouselState, 150);
});