"""Рекомендовані розміри зображень для адмінки та ліміти стиснення."""

from typing import NamedTuple


class ImageLimit(NamedTuple):
    """Максимальний розмір файлу після збереження. Менші зображення не збільшуються."""

    max_width: int
    max_height: int
    quality: int


# Формат: (ширина, висота, співвідношення, додаткова підказка)
MODEL_IMAGE = (
    '1600×1200 px (4:3), JPG/PNG/WebP. '
    'Для карток каталогу достатньо 960×640. '
    'Одне фото позначте «Головне» — воно буде першим на сайті.'
)
MODEL_IMAGE_LIMIT = ImageLimit(1600, 1600, 82)

FLOOR_PLAN_IMAGE = (
    '880×880 px (квадрат), PNG або JPG з прозорим/світлим фоном. '
    'На сайті відображається до 520 px ширини (object-fit: contain).'
)
FLOOR_PLAN_LIMIT = ImageLimit(1400, 1400, 90)

BLOG_COVER_IMAGE = (
    '1520×800 px (~16:9) для сторінки статті; мінімум 1200×630 px. '
    'У списку блогу обрізається до висоти 200 px (object-fit: cover).'
)
BLOG_COVER_LIMIT = ImageLimit(1520, 800, 82)

GALLERY_IMAGE = (
    '1200×900 px (4:3), JPG/PNG/WebP. '
    'Для lightbox бажано до 1800×1350 px. '
    'На сайті — сітка masonry з crop 4:3.'
)
GALLERY_LIMIT = ImageLimit(1800, 1800, 82)

TEAM_PHOTO_IMAGE = (
    '800×800 px (квадрат), JPG/PNG/WebP, портрет по плечі. '
    'Без фото — на сайті показуються ініціали на кольоровому фоні.'
)
TEAM_PHOTO_LIMIT = ImageLimit(800, 800, 82)

IMAGE_FORMAT_HINT = (
    'Можна завантажити JPG, PNG або WebP. '
    'Після збереження файл зменшується до ліміту поля і зберігається як WebP.'
)
