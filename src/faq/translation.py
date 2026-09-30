from modeltranslation.translator import translator, TranslationOptions

from .models import FAQGroup, FAQItem


class FAQGroupTranslationOptions(TranslationOptions):
    fields = ('name',)
    fallback_undefined = None


class FAQItemTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
    fallback_undefined = None


translator.register(FAQGroup, FAQGroupTranslationOptions)
translator.register(FAQItem, FAQItemTranslationOptions)
