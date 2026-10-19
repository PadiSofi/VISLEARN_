(() => {
    'use strict';

    const root = document.documentElement;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const hasObserver = 'IntersectionObserver' in window;
    const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

    /* 1. Titulares palabra por palabra (data-split) */
    function splitWords() {
        document.querySelectorAll('[data-split]').forEach((el) => {
            const text = el.textContent.trim().replace(/\s+/g, ' ');
            el.setAttribute('aria-label', text);
            el.textContent = '';
            const words = text.split(' ');
            words.forEach((word, i) => {
                const outer = document.createElement('span');
                outer.className = 'split-word';
                outer.setAttribute('aria-hidden', 'true');
                const inner = document.createElement('span');
                inner.className = 'split-word__inner';
                inner.style.setProperty('--i', i);
                inner.textContent = word;
                outer.appendChild(inner);
                el.appendChild(outer);
                if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
            });
        });
    }

    /* 2. Revelados (data-reveal, data-reveal-stagger, data-reveal-alternate) */
    function prepareReveals() {
        document.querySelectorAll('[data-reveal-stagger]').forEach((group) => {
            const effect = group.dataset.revealStagger || 'up';
            [...group.children].forEach((child, i) => {
                if (!child.dataset.reveal) child.dataset.reveal = effect;
                child.style.setProperty('--reveal-delay', `${Math.min(i, 6) * 90}ms`);
            });
        });
        document.querySelectorAll('[data-reveal-alternate]').forEach((group) => {
            [...group.children].forEach((child, i) => {
                if (!child.dataset.reveal) child.dataset.reveal = i % 2 === 0 ? 'left' : 'right';
            });
        });
    }

    function initReveals() {
        const targets = document.querySelectorAll('[data-reveal], [data-split]');

        if (reduceMotion || !hasObserver) {
            targets.forEach((el) => {
                el.classList.add('is-revealed');
                el.removeAttribute('data-reveal');
            });
            return;
        }

        const reveal = (el) => {
            el.classList.add('is-revealed');
            if (el.hasAttribute('data-reveal')) {
                const delay = parseFloat(getComputedStyle(el).getPropertyValue('--reveal-delay')) || 0;
                // Al terminar la animación se quita el atributo para que el elemento
                // recupere su propio CSS (por ejemplo, el efecto hover de las tarjetas)
                window.setTimeout(() => {
                    el.removeAttribute('data-reveal');
                    el.style.removeProperty('--reveal-delay');
                }, delay + 1100);
            }
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                observer.unobserve(entry.target);
                reveal(entry.target);
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -6% 0px' });

        targets.forEach((el) => observer.observe(el));
    }

    /* 3. Contadores (data-count-to) */
    function initCounters() {
        const counters = document.querySelectorAll('[data-count-to]');
        if (!counters.length || reduceMotion || !hasObserver) return;

        const run = (el) => {
            const target = parseInt(el.dataset.countTo, 10) || 0;
            const duration = 1600;
            const start = performance.now();
            const tick = (now) => {
                const t = clamp((now - start) / duration, 0, 1);
                const eased = 1 - Math.pow(1 - t, 3);
                el.textContent = Math.round(target * eased).toLocaleString('es-CO');
                if (t < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                observer.unobserve(entry.target);
                run(entry.target);
            });
        }, { threshold: 0.6 });

        counters.forEach((el) => {
            el.textContent = '0';
            observer.observe(el);
        });
    }

    /* 4. Escena fija (data-story) */
    function initStory(story) {
        const sticky = story.querySelector('.story__sticky');
        const panels = [...story.querySelectorAll('.story__panel')];
        const items = [...story.querySelectorAll('.story__rail-item')];
        const steps = panels.length;
        let current = -1;

        const metrics = () => ({
            stickyTop: parseFloat(getComputedStyle(sticky).top) || 0,
            distance: Math.max(1, story.offsetHeight - sticky.offsetHeight),
        });

        // Clic en un paso del riel: desplaza la página hasta ese paso
        items.forEach((item, i) => {
            item.addEventListener('click', () => {
                const { stickyTop, distance } = metrics();
                const storyTop = window.scrollY + story.getBoundingClientRect().top;
                window.scrollTo({
                    top: storyTop - stickyTop + ((i + 0.5) / steps) * distance,
                    behavior: reduceMotion ? 'auto' : 'smooth',
                });
            });
        });

        return function update() {
            const { stickyTop, distance } = metrics();
            const progress = clamp((stickyTop - story.getBoundingClientRect().top) / distance, 0, 1);
            story.style.setProperty('--story-progress', progress.toFixed(3));

            const index = Math.min(steps - 1, Math.floor(progress * steps));
            if (index === current) return;
            current = index;

            panels.forEach((panel, i) => {
                panel.classList.toggle('is-active', i === index);
                panel.classList.toggle('is-past', i < index);
            });
            items.forEach((item, i) => {
                item.classList.toggle('is-active', i === index);
                item.classList.toggle('is-done', i < index);
                item.setAttribute('aria-current', i === index ? 'step' : 'false');
            });
        };
    }

    /* 5. Bucle de scroll (un solo requestAnimationFrame para todo) */
    function init() {
        splitWords();
        prepareReveals();
        initReveals();
        initCounters();

        const progressBar = document.getElementById('scroll-progress');
        const parallaxEls = [...document.querySelectorAll('[data-parallax]')];
        const scrollOutEls = [...document.querySelectorAll('[data-scroll-out]')];
        const stories = [...document.querySelectorAll('[data-story]')].map(initStory);

        let ticking = false;

        function update() {
            ticking = false;
            const viewport = window.innerHeight;

            if (progressBar) {
                const max = root.scrollHeight - viewport;
                progressBar.style.transform = `scaleX(${max > 0 ? clamp(window.scrollY / max, 0, 1) : 0})`;
            }

            if (!reduceMotion) {
                // Parallax: la capa se mueve más lento que el scroll y nunca deja huecos
                parallaxEls.forEach((el) => {
                    const box = el.parentElement;
                    const rect = box.getBoundingClientRect();
                    if (rect.bottom < 0 || rect.top > viewport) return;
                    const speed = parseFloat(el.dataset.parallax) || 0.2;
                    const scale = parseFloat(el.dataset.parallaxScale) || 1;
                    const maxShift = Math.max(0, (el.offsetHeight * scale - box.offsetHeight) / 2);
                    const shift = clamp((rect.top + rect.height / 2 - viewport / 2) * -speed, -maxShift, maxShift);
                    el.style.transform = `translate3d(0, ${shift.toFixed(1)}px, 0) scale(${scale})`;
                });

                // Contenido que se desvanece mientras su sección se va
                scrollOutEls.forEach((el) => {
                    const section = el.closest('section') || el.parentElement;
                    const rect = section.getBoundingClientRect();
                    if (rect.bottom < 0) return;
                    const p = clamp(-rect.top / (rect.height * 0.6), 0, 1);
                    el.style.opacity = (1 - p).toFixed(3);
                    el.style.transform = `translate3d(0, ${(p * 60).toFixed(1)}px, 0)`;
                });
            }

            stories.forEach((updateStory) => updateStory());
        }

        const requestTick = () => {
            if (!ticking) {
                ticking = true;
                requestAnimationFrame(update);
            }
        };

        window.addEventListener('scroll', requestTick, { passive: true });
        window.addEventListener('resize', requestTick);
        update();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
