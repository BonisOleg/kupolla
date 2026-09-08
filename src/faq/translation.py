from modeltranslation.translator import translator, TranslationOptions

from .models import FAQGroup, FAQItem


class FAQGroupTranslationOptions(TranslationOptions):
    fields = ('name',)


class FAQItemTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


translator.register(FAQGroup, FAQGroupTranslationOptions)
translator.register(FAQItem, FAQItemTranslationOptions)
