document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.site-header');
    if (header) {
        window.addEventListener('scroll', () => {
            header.classList.toggle('scrolled', window.scrollY > 20);
        });
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, { threshold: 0.1 });

    // --- MENÚ SITIO PÚBLICO (base.html) ---
    const toggle = document.getElementById('nav-toggle');
    const nav = document.getElementById('main-nav');
    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            nav.classList.toggle('is-open');
            const icon = toggle.querySelector('.material-symbols-outlined');
            if (icon) {
                icon.textContent = nav.classList.contains('is-open') ? 'close' : 'menu';
            }
        });
    }

    // --- MENÚ DASHBOARD (dashboard_base.html) ---
    const appToggle = document.getElementById('app-nav-toggle');
    const appNav = document.getElementById('app-nav');
    if (appToggle && appNav) {
        appToggle.addEventListener('click', () => {
            appNav.classList.toggle('is-open');
            const icon = appToggle.querySelector('.material-symbols-outlined');
            if (icon) {
                icon.textContent = appNav.classList.contains('is-open') ? 'close' : 'menu';
            }
        });
    }

    // El dropdown "Conócenos" en móvil
    const dropdownToggle = document.querySelector('.nav-dropdown__toggle');
    if (dropdownToggle && window.innerWidth < 768) {
        dropdownToggle.addEventListener('click', (e) => {
            e.preventDefault();
            const dropdownMenu = dropdownToggle.nextElementSibling;
            if (dropdownMenu) {
                dropdownMenu.classList.toggle('is-open');
            }
        });
    }

    const notifToggle = document.getElementById('notif-toggle');
    const notifDropdown = document.getElementById('notif-dropdown');
    if (notifToggle && notifDropdown) {
        notifToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            notifDropdown.classList.toggle('is-open');
        });
        document.addEventListener('click', (e) => {
            if (!notifDropdown.contains(e.target) && !notifToggle.contains(e.target)) {
                notifDropdown.classList.remove('is-open');
            }
        });
    }

    document.querySelectorAll('.fade-in-up').forEach(el => observer.observe(el));
});

