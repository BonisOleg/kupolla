from modeltranslation.translator import translator, TranslationOptions

from .models import Category, Tag, Post


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    fallback_undefined = None


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)
    fallback_undefined = None


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'body', 'seo_title', 'seo_description')
    fallback_undefined = None


translator.register(Category, CategoryTranslationOptions)
translator.register(Tag, TagTranslationOptions)
translator.register(Post, PostTranslationOptions)
