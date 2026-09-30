from modeltranslation.translator import translator, TranslationOptions

from .models import ConfigOption


class ConfigOptionTranslationOptions(TranslationOptions):
    fields = ('name',)
    fallback_undefined = None


translator.register(ConfigOption, ConfigOptionTranslationOptions)
