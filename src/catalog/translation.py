from modeltranslation.translator import translator, TranslationOptions

from .models import DomeModel, ModelSpec


class DomeModelTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description', 'floor_plan_note')


class ModelSpecTranslationOptions(TranslationOptions):
    fields = ('key', 'value')


translator.register(DomeModel, DomeModelTranslationOptions)
translator.register(ModelSpec, ModelSpecTranslationOptions)
