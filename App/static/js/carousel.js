document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('carouselContainer');
  const cards = Array.from(document.querySelectorAll('.carousel-card'));
  const leftBtn = document.getElementById('scrollLeft');
  const rightBtn = document.getElementById('scrollRight');
  const progressBar = document.getElementById('scrollProgressBar');

  if (!container || cards.length === 0) return;

  // ---- Prevent native image ghost-dragging / text selection ----
  container.querySelectorAll('img').forEach((img) => {
    img.setAttribute('draggable', 'false');
    img.addEventListener('dragstart', (e) => e.preventDefault());
  });

  const CARD_WIDTH = 300;
  const CARD_GAP = 32; // 2rem
  const scrollAmount = CARD_WIDTH + CARD_GAP;

  // ---- Cache card centers ONCE (and on resize) instead of measuring on every scroll ----
  // getBoundingClientRect() inside a scroll handler forces the browser to
  // recompute layout on every single scroll event -> main-thread jank.
  // offsetLeft is stable here because cards have a fixed flex-basis/height,
  // so we can precompute and do pure arithmetic during scroll.
  let cardCenters = [];
  let maxScroll = 0;

  function measure() {
    maxScroll = container.scrollWidth - container.clientWidth;
    cardCenters = cards.map((card) => card.offsetLeft + card.offsetWidth / 2);
  }

  // ---- Active card + progress bar, batched to one rAF per frame ----
  let activeIndex = -1;
  let scrollTicking = false;

  function applyActiveCard() {
    scrollTicking = false;

    const viewportCenter = container.scrollLeft + container.clientWidth / 2;

    let nearestIndex = 0;
    let nearestDist = Infinity;
    for (let i = 0; i < cardCenters.length; i++) {
      const dist = Math.abs(cardCenters[i] - viewportCenter);
      if (dist < nearestDist) {
        nearestDist = dist;
        nearestIndex = i;
      }
    }

    if (nearestIndex !== activeIndex) {
      if (activeIndex !== -1) cards[activeIndex].classList.remove('active');
      cards[nearestIndex].classList.add('active');
      activeIndex = nearestIndex;
    }

    if (progressBar && maxScroll > 0) {
      const percent = container.scrollLeft / maxScroll;
      // Bar is 30% of track width, so its travel range is (100/30 - 1) * 100%
      progressBar.style.transform = `translateX(${percent * 233.33}%)`;
    }
  }

  function onScroll() {
    if (!scrollTicking) {
      scrollTicking = true;
      requestAnimationFrame(applyActiveCard);
    }
  }

  container.addEventListener('scroll', onScroll, { passive: true });

  let resizeTimer = null;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      measure();
      onScroll();
    }, 150);
  });

  // ---- Button navigation ----
  if (leftBtn) {
    leftBtn.addEventListener('click', () => {
      container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });
  }
  if (rightBtn) {
    rightBtn.addEventListener('click', () => {
      container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
  }

  // ---- Pointer-based drag (desktop mouse only — touch keeps native momentum scroll) ----
  // Using Pointer Events (instead of separate mouse handlers) with pointer
  // capture means we keep receiving move/up events even if the cursor
  // leaves the container mid-drag, so there's no "stuck dragging" state.
  // The scrollLeft write is deferred into a rAF so it happens at most once
  // per frame instead of once per mousemove (mousemove can fire far more
  // often than 60Hz on some devices).
  let isPointerDown = false;
  let isDragging = false;
  let dragStartX = 0;
  let dragStartScroll = 0;
  let pendingScrollLeft = null;
  let dragTicking = false;
  const DRAG_THRESHOLD = 5;

  function applyDragScroll() {
    dragTicking = false;
    if (pendingScrollLeft === null) return;
    container.scrollLeft = pendingScrollLeft;
    pendingScrollLeft = null;
  }

  container.addEventListener('pointerdown', (e) => {
    if (e.pointerType !== 'mouse' || e.button !== 0) return; // let touch/pen use native scrolling

    isPointerDown = true;
    isDragging = false;
    dragStartX = e.clientX;
    dragStartScroll = container.scrollLeft;
    container.classList.add('is-dragging');
    container.setPointerCapture(e.pointerId);
  });

  container.addEventListener('pointermove', (e) => {
    if (!isPointerDown) return;

    const delta = e.clientX - dragStartX;

    if (!isDragging) {
      if (Math.abs(delta) < DRAG_THRESHOLD) return;
      isDragging = true;
    }

    e.preventDefault();
    pendingScrollLeft = dragStartScroll - delta * 1.2;

    if (!dragTicking) {
      dragTicking = true;
      requestAnimationFrame(applyDragScroll);
    }
  });

  function endDrag(e) {
    if (!isPointerDown) return;
    isPointerDown = false;
    container.classList.remove('is-dragging');
    try {
      container.releasePointerCapture(e.pointerId);
    } catch (err) {
      /* pointer already released */
    }
  }

  container.addEventListener('pointerup', endDrag);
  container.addEventListener('pointercancel', endDrag);

  // Suppress the card's click-through (opening the lightbox) right after a drag
  cards.forEach((card) => {
    card.addEventListener(
      'click',
      (e) => {
        if (isDragging) {
          e.stopImmediatePropagation();
          e.preventDefault();
          isDragging = false;
        }
      },
      true,
    );
  });

  // ---- Init ----
  measure();
  requestAnimationFrame(applyActiveCard);
});