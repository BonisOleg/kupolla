"""Контекст головної сторінки адмінки (DASHBOARD_CALLBACK)."""

from datetime import timedelta

from django.db.models import Count
from django.urls import reverse
from django.utils import timezone

from src.blog.models import Post
from src.catalog.models import DomeModel
from src.gallery.models import GalleryPhoto
from src.leads.models import Lead


def admin_dashboard_callback(request, context):
    today = timezone.localdate()
    week_ago = timezone.now() - timedelta(days=7)

    new_leads = Lead.objects.filter(status=Lead.Status.NEW).count()
    leads_week = Lead.objects.filter(created_at__gte=week_ago).count()
    unpublished_posts = Post.objects.filter(is_published=False).count()
    draft_models = DomeModel.objects.filter(is_published=False).count()
    gallery_drafts = GalleryPhoto.objects.filter(is_published=False).count()

    leads_by_status = (
        Lead.objects.values('status')
        .annotate(total=Count('id'))
        .order_by('status')
    )
    status_labels = dict(Lead.Status.choices)
    lead_status_stats = [
        {
            'label': status_labels.get(row['status'], row['status']),
            'total': row['total'],
        }
        for row in leads_by_status
    ]

    context['dashboard'] = {
        'greeting': _greeting(request),
        'stats': [
            {
                'title': 'Нові заявки',
                'value': new_leads,
                'icon': 'inbox',
                'accent': 'primary' if new_leads else 'default',
                'link': reverse('admin:leads_lead_changelist') + '?status__exact=new',
            },
            {
                'title': 'Заявки за 7 днів',
                'value': leads_week,
                'icon': 'calendar_today',
                'accent': 'default',
                'link': reverse('admin:leads_lead_changelist'),
            },
            {
                'title': 'Чернетки статей',
                'value': unpublished_posts,
                'icon': 'article',
                'accent': 'warning' if unpublished_posts else 'default',
                'link': reverse('admin:blog_post_changelist') + '?is_published__exact=0',
            },
            {
                'title': 'Моделі не опубліковані',
                'value': draft_models,
                'icon': 'home',
                'accent': 'warning' if draft_models else 'default',
                'link': reverse('admin:catalog_domemodel_changelist') + '?is_published__exact=0',
            },
            {
                'title': 'Фото галереї (чернетки)',
                'value': gallery_drafts,
                'icon': 'photo_library',
                'accent': 'default',
                'link': reverse('admin:gallery_galleryphoto_changelist') + '?is_published__exact=0',
            },
        ],
        'quick_links': [
            {
                'title': 'Налаштування сайту',
                'icon': 'settings',
                'link': reverse('admin:core_sitesettings_changelist'),
                'hint': 'Контакти, CRM, соцмережі',
            },
            {
                'title': 'Моделі куполів',
                'icon': 'home',
                'link': reverse('admin:catalog_domemodel_changelist'),
                'hint': 'Каталог, ціни, фото',
            },
            {
                'title': 'Конфігуратор',
                'icon': 'tune',
                'link': reverse('admin:configurator_configoption_changelist'),
                'hint': 'Опції та ціни',
            },
            {
                'title': 'Заявки',
                'icon': 'inbox',
                'link': reverse('admin:leads_lead_changelist'),
                'hint': 'CRM та статуси',
            },
            {
                'title': 'Блог',
                'icon': 'newspaper',
                'link': reverse('admin:blog_post_changelist'),
                'hint': 'Статті та публікації',
            },
            {
                'title': 'FAQ',
                'icon': 'help',
                'link': reverse('admin:faq_faqgroup_changelist'),
                'hint': 'Групи та питання',
            },
        ],
        'lead_status_stats': lead_status_stats,
        'today': today,
    }
    return context


def _greeting(request):
    hour = timezone.localtime().hour
    name = request.user.get_short_name() or request.user.username
    if hour < 12:
        prefix = 'Доброго ранку'
    elif hour < 18:
        prefix = 'Доброго дня'
    else:
        prefix = 'Доброго вечора'
    return f'{prefix}, {name}'
