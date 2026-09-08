from modeltranslation.translator import translator, TranslationOptions

from .models import GalleryPhoto


class GalleryPhotoTranslationOptions(TranslationOptions):
    fields = ('title', 'alt')


translator.register(GalleryPhoto, GalleryPhotoTranslationOptions)
