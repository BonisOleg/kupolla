from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from src.core.i18n import collapse_double_prefix, localize_path, strip_language_prefix


class I18nPathTests(SimpleTestCase):
    def test_strip_and_localize(self):
        self.assertEqual(strip_language_prefix('/uk/about/'), '/about/')
        self.assertEqual(localize_path('/uk/about/', 'en'), '/en/about/')
        self.assertEqual(localize_path('/en/about/', 'uk'), '/about/')
        self.assertEqual(localize_path('/', 'uk'), '/')

    def test_collapse_double_prefix(self):
        self.assertEqual(collapse_double_prefix('/uk/en/about/'), '/en/about/')
        self.assertEqual(collapse_double_prefix('/en/about/'), '/en/about/')


class LanguageSwitcherTests(TestCase):
    def test_set_language_keeps_current_path(self):
        response = self.client.post(
            reverse('set_language'),
            {'language': 'en', 'next': '/uk/contacts/'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/en/contacts/')

    def test_uk_prefix_redirects_home(self):
        response = self.client.get('/uk/about/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], '/about/')

    def test_disabled_language_redirects_to_ukrainian(self):
        response = self.client.get('/fr/faq/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/faq/')

    def test_enabled_english_stays(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)

    def test_home_has_hreflang_and_canonical(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, 'hreflang="en"')
        self.assertContains(response, 'hreflang="uk"')
        self.assertNotContains(response, 'hreflang="fr"')
        self.assertNotContains(response, '/uk/')
        self.assertContains(response, 'data-qa="lang-switch"')
        self.assertContains(response, 'data-qa="lead-form"')
        self.assertContains(response, 'data-qa="menu-open"')
        self.assertContains(response, 'name="csrf-token"')
        self.assertContains(response, 'htmx.min.js')
        self.assertNotContains(response, 'unpkg.com/htmx')
