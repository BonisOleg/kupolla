from modeltranslation.translator import translator, TranslationOptions

from .models import Category, Tag, Post


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'body', 'seo_title', 'seo_description')


translator.register(Category, CategoryTranslationOptions)
translator.register(Tag, TagTranslationOptions)
translator.register(Post, PostTranslationOptions)
