from django.test import TestCase


class PublicUrlSmokeTests(TestCase):
    """Перевірка доступності ключових сторінок."""

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_healthcheck(self):
        response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_favicon_redirect(self):
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 301)
        self.assertIn('/static/favicon.ico', response['Location'])

    def test_contacts_page(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_configurator_page(self):
        response = self.client.get('/configurator/')
        self.assertEqual(response.status_code, 200)

    def test_calculate_api(self):
        response = self.client.post(
            '/api/configurator/calculate/',
            data={'model': 'kupolla-s', 'tier': 'base', 'addons': []},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.json())

    def test_models_list_page(self):
        """/models/ — модельний ряд (Compact/Prime/Grand), а не редірект."""
        response = self.client.get('/models/', follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertIn('models', response.context)
        slugs = {dome.slug for dome in response.context['models']}
        self.assertEqual(slugs, {'kupolla-compact', 'kupolla-s', 'kupolla-grand'})
