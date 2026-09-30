from modeltranslation.translator import translator, TranslationOptions

from .models import GalleryPhoto


class GalleryPhotoTranslationOptions(TranslationOptions):
    fields = ('title', 'alt')
    fallback_undefined = None


translator.register(GalleryPhoto, GalleryPhotoTranslationOptions)
