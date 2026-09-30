from django.db import IntegrityError, transaction
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.test import RequestFactory, TestCase
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core.admin import GroupAdmin, UserAdmin
from src.core.models import SiteSettings
from src.faq.models import FAQGroup
from src.pages.models import AboutPage, TechnologiesPage


def _request(user):
    request = RequestFactory().post('/admin/auth/user/')
    request.user = user
    request.session = {}
    request._messages = FallbackStorage(request)
    return request


class UnfoldAuthAdminTests(TestCase):
    def test_user_and_group_use_unfold_mro(self):
        self.assertLess(UserAdmin.__mro__.index(BaseUserAdmin), UserAdmin.__mro__.index(ModelAdmin))
        self.assertLess(GroupAdmin.__mro__.index(BaseGroupAdmin), GroupAdmin.__mro__.index(ModelAdmin))
        self.assertIsInstance(admin.site._registry[User], UserAdmin)

    def test_sidebar_links_users_and_groups(self):
        user = User.objects.create_superuser('keeper', 'keeper@kupolla.test', 'Kupolla-admin-1')
        self.client.force_login(user)
        response = self.client.get('/admin/')
        self.assertContains(response, reverse('admin:auth_user_changelist'))
        self.assertContains(response, reverse('admin:auth_group_changelist'))
        self.assertContains(response, 'kupolla-dashboard.css')
        self.assertContains(response, 'kp-admin-dash')
        self.assertNotContains(response, 'xl:grid-cols-5')

    def test_delete_guards(self):
        keeper = User.objects.create_superuser('keeper', 'keeper@kupolla.test', 'Kupolla-admin-1')
        other = User.objects.create_superuser('other', 'other@kupolla.test', 'Kupolla-admin-1')
        staff = User.objects.create_user('staff', 'staff@kupolla.test', 'Kupolla-admin-1', is_staff=True)
        modeladmin = UserAdmin(User, admin.site)
        request = _request(keeper)

        self.assertFalse(modeladmin.has_delete_permission(request, keeper))
        with self.assertRaises(PermissionDenied):
            modeladmin.delete_model(request, keeper)

        staff_request = _request(staff)
        modeladmin.delete_queryset(staff_request, User.objects.filter(pk__in=[keeper.pk, other.pk]))
        self.assertTrue(User.objects.filter(pk=keeper.pk).exists())
        self.assertTrue(User.objects.filter(pk=other.pk).exists())

        modeladmin.delete_queryset(request, User.objects.filter(pk=staff.pk))
        self.assertFalse(User.objects.filter(pk=staff.pk).exists())


class SingletonModelTests(TestCase):
    def test_save_forces_pk_and_blocks_delete(self):
        settings = SiteSettings.load()
        settings.company_name = 'KUPOLLA'
        settings.pk = 9
        settings.save()
        self.assertEqual(settings.pk, 1)
        self.assertEqual(SiteSettings.objects.count(), 1)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SiteSettings.objects.bulk_create([SiteSettings(pk=2, company_name='other')])
        with self.assertRaises(ProtectedError):
            SiteSettings.objects.get(pk=1).delete()
        with self.assertRaises(ProtectedError):
            AboutPage.load().delete()
        TechnologiesPage.load()
        with self.assertRaises(ProtectedError):
            TechnologiesPage.objects.filter(pk=1).delete()
        self.assertEqual(SiteSettings.objects.none().delete(), (0, {}))

    def test_team_lives_on_about_form_only(self):
        user = User.objects.create_superuser('keeper', 'keeper@kupolla.test', 'Kupolla-admin-1')
        self.client.force_login(user)
        about = AboutPage.load()
        change = self.client.get(reverse('admin:pages_aboutpage_change', args=[about.pk]))
        self.assertEqual(change.status_code, 200)
        self.assertContains(change, 'Команда на сторінці')
        self.assertEqual(self.client.get('/admin/pages/teammember/').status_code, 404)
        self.assertEqual(self.client.get('/admin/faq/faqitem/').status_code, 404)
        group = FAQGroup.objects.order_by('pk').first()
        self.assertIsNotNone(group)
        faq = self.client.get(reverse('admin:faq_faqgroup_change', args=[group.pk]))
        self.assertEqual(faq.status_code, 200)
        self.assertContains(faq, 'Питання цієї групи')
