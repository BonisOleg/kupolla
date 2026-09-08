from modeltranslation.translator import translator, TranslationOptions

from .models import ConfigOption


class ConfigOptionTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ConfigOption, ConfigOptionTranslationOptions)
