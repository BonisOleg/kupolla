from django.core.management.base import BaseCommand

from src.core.image_compress import compress_saved_media


class Command(BaseCommand):
    help = 'Конвертує зображення моделей у WebP і зменшує ті, що більші за ліміт поля.'

    def handle(self, *args, **options):
        stats = compress_saved_media()
        for line in stats.changes:
            self.stdout.write(line)
        for line in stats.errors:
            self.stderr.write(line)
        self.stdout.write(
            self.style.SUCCESS(
                f'Готово: конвертовано {stats.converted}, '
                f'пропущено {stats.skipped}, немає файлу {stats.missing}.'
            )
        )
