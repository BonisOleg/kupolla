from modeltranslation.translator import translator, TranslationOptions

from .models import AboutPage, TeamMember, TechnologiesPage


class AboutPageTranslationOptions(TranslationOptions):
    fields = ('mission_title', 'mission_body', 'values_body', 'cooperation_body', 'team_body', 'cta_title')
    fallback_undefined = None


class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('position',)
    fallback_undefined = None


class TechnologiesPageTranslationOptions(TranslationOptions):
    fields = ('intro_body', 'construction_body', 'materials_body', 'energy_body', 'production_body', 'certificates_body')
    fallback_undefined = None


translator.register(AboutPage, AboutPageTranslationOptions)
translator.register(TeamMember, TeamMemberTranslationOptions)
translator.register(TechnologiesPage, TechnologiesPageTranslationOptions)
