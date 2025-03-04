import os
from io import BytesIO
from PIL import Image
import hashlib
from django.core.files import File




def delete_image_methods(field_name):
    if field_name:
        file_path = field_name.path
        if os.path.isfile(file_path):
            os.remove(file_path)


def process_save_image(model_instance, save_method, cls, *args, **kwargs):
    model_field = model_instance.image
    model_pk = model_instance.pk or None

    if model_pk:
        try:
            # Получаем старое изображение для проверки
            old_image = cls.objects.get(pk=model_pk)
            if old_image.image and old_image.image != model_field:
                        # Удаляем старое изображение, если оно существует и отличается
                delete_image_methods(old_image.image)
            else:
                return save_method.save(*args, **kwargs)
        except cls.DoesNotExist:
                pass

        # Открываем изображение
    img = Image.open(model_field)

    # Удаляем метаданные (например, EXIF)
    img_data = img.getdata()
    img.putdata(img_data)

    # Конвертируем изображение в RGB перед сохранением в WebP
    img = img.convert('RGB')
    webp_image = BytesIO()
    img.save(webp_image, format='WEBP')

    # Генерация уникального хеша для имени файла
    img_hashname = hashlib.md5(webp_image.getvalue()).hexdigest()

    # Возвращаем к началу файла после записи
    webp_image.seek(0)

    if webp_image:
        webp_image.seek(0)  # Возвращаемся к началу файла после записи
        model_field.save(f"{img_hashname}.webp", File(webp_image), save=False)  # Сохраняем как WebP

    save_method.save(*args, **kwargs)