from unittest.mock import patch

from django.test import TestCase

from src.leads.models import Lead


class LeadFormViewTests(TestCase):
    def _post_lead(self, extra=None):
        data = {
            'form_type': 'hero',
            'name': 'Тест Тестович',
            'phone': '+380501234567',
            'email': 'test@example.com',
            'gdpr_consent': 'on',
        }
        if extra:
            data.update(extra)
        return self.client.post(
            '/api/forms/',
            data=data,
            HTTP_HX_REQUEST='true',
        )

    @patch('src.leads.signals.requests.post')
    def test_valid_lead_is_saved(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = lambda: None

        before = Lead.objects.count()
        response = self._post_lead()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), before + 1)
        self.assertContains(response, 'kp-form__success')

    @patch('src.leads.signals.requests.post')
    def test_placeholder_crm_url_is_not_called(self, mock_post):
        response = self._post_lead()
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()

    def test_honeypot_is_not_saved(self):
        before = Lead.objects.count()
        response = self._post_lead({'website': 'http://spam.test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), before)
        self.assertContains(response, 'kp-form__success')

    def test_invalid_phone_is_rejected(self):
        response = self._post_lead({'phone': '000'})
        self.assertEqual(response.status_code, 422)
        self.assertNotIn(b'kp-form__success', response.content)

    @patch('src.leads.signals.requests.post')
    def test_country_and_city_are_saved(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = lambda: None

        response = self._post_lead({'country': 'Україна', 'city': 'Київ'})
        self.assertEqual(response.status_code, 200)
        lead = Lead.objects.latest('created_at')
        self.assertEqual(lead.country, 'Україна')
        self.assertEqual(lead.city, 'Київ')

    @patch('src.leads.signals.requests.post')
    def test_country_and_city_are_optional(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = lambda: None

        response = self._post_lead()
        self.assertEqual(response.status_code, 200)
        lead = Lead.objects.latest('created_at')
        self.assertEqual(lead.country, '')
        self.assertEqual(lead.city, '')
