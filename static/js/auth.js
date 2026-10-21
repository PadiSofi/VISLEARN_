(() => {
    'use strict';

    /* Mostrar / ocultar contraseña */
    document.querySelectorAll('[data-toggle-password]').forEach((button) => {
        const input = button.parentElement.querySelector('input');
        if (!input) return;
        button.addEventListener('click', () => {
            const mostrar = input.type === 'password';
            input.type = mostrar ? 'text' : 'password';
            button.setAttribute('aria-label', mostrar ? 'Ocultar contraseña' : 'Mostrar contraseña');
            button.querySelector('.material-symbols-outlined').textContent = mostrar ? 'visibility_off' : 'visibility';
        });
    });

    /* Medidor de fortaleza (solo ayuda visual: las reglas reales las valida el servidor) */
    const meter = document.querySelector('[data-pw-meter]');
    const pw1 = document.getElementById('id_password1');
    const pw2 = document.getElementById('id_password2');
    const matchText = document.querySelector('[data-pw-match]');
    const etiquetas = ['', 'Débil', 'Aceptable', 'Buena', 'Fuerte'];

    function nivel(clave) {
        if (!clave) return 0;
        let puntos = 0;
        if (clave.length >= 8) puntos++;
        if (/[a-z]/.test(clave) && /[A-Z]/.test(clave)) puntos++;
        if (/\d/.test(clave)) puntos++;
        if (/[^A-Za-z0-9]/.test(clave)) puntos++;
        return clave.length < 8 ? 1 : Math.max(puntos, 1);
    }

    function actualizarCoincidencia() {
        if (!matchText || !pw1 || !pw2) return;
        if (!pw2.value) {
            matchText.textContent = '';
            return;
        }
        const coinciden = pw1.value === pw2.value;
        matchText.textContent = coinciden ? 'Las contraseñas coinciden' : 'Las contraseñas no coinciden';
        matchText.className = 'auth-help ' + (coinciden ? 'auth-help--ok' : 'auth-help--bad');
    }

    if (meter && pw1) {
        const label = meter.querySelector('.pw-meter__label');
        pw1.addEventListener('input', () => {
            const n = nivel(pw1.value);
            meter.dataset.level = n;
            label.textContent = etiquetas[n];
            actualizarCoincidencia();
        });
    }
    if (pw2) pw2.addEventListener('input', actualizarCoincidencia);
})();