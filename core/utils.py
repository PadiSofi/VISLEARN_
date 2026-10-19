import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

EXTENSIONES_IMAGEN = ('.jpg', '.jpeg', '.png')


def optimizar_imagen(archivo, max_lado=1600, calidad=80):
    """Reduce el tamaño y el peso de una imagen subida. Los PDF y otros archivos no se tocan."""
    nombre, extension = os.path.splitext(os.path.basename(archivo.name))
    if extension.lower() not in EXTENSIONES_IMAGEN:
        return archivo

    try:
        imagen = Image.open(archivo)
        imagen = ImageOps.exif_transpose(imagen)  # respeta la orientación de fotos de celular
        imagen.thumbnail((max_lado, max_lado))    # nunca agranda, solo reduce

        tiene_transparencia = imagen.mode in ('RGBA', 'LA') or (
            imagen.mode == 'P' and 'transparency' in imagen.info
        )
        buffer = BytesIO()
        if tiene_transparencia:
            imagen.convert('RGBA').save(buffer, format='PNG', optimize=True)
            nuevo_nombre = f'{nombre}.png'
        else:
            imagen.convert('RGB').save(buffer, format='JPEG', quality=calidad, optimize=True)
            nuevo_nombre = f'{nombre}.jpg'
        return ContentFile(buffer.getvalue(), name=nuevo_nombre)
    except Exception:
        try:
            archivo.seek(0)
        except Exception:
            pass
        return archivo  # si algo falla, se guarda el original sin cambios
