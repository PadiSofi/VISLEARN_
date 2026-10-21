import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def formato_articulo(texto):
    """Convierte texto plano en HTML seguro: párrafos, '## subtítulos' y '- viñetas'."""
    bloques = re.split(r'\n\s*\n', texto.replace('\r\n', '\n').strip())
    html = []
    for bloque in bloques:
        lineas = [linea.strip() for linea in bloque.split('\n') if linea.strip()]
        if not lineas:
            continue
        if lineas[0].startswith('## '):
            html.append(f'<h2>{escape(lineas[0][3:])}</h2>')
            lineas = lineas[1:]
            if not lineas:
                continue
        if all(linea.startswith('- ') for linea in lineas):
            items = ''.join(f'<li>{escape(linea[2:])}</li>' for linea in lineas)
            html.append(f'<ul>{items}</ul>')
        else:
            html.append('<p>' + '<br>'.join(escape(linea) for linea in lineas) + '</p>')
    return mark_safe('\n'.join(html))
