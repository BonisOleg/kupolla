from django.test import SimpleTestCase

from src.core.crm import build_lead_payload, is_configured_crm_webhook


class CrmWebhookValidationTests(SimpleTestCase):
    def test_empty_url_is_not_configured(self):
        self.assertFalse(is_configured_crm_webhook(''))

    def test_placeholder_make_url_is_rejected(self):
        self.assertFalse(is_configured_crm_webhook('https://hook.eu2.make.com/kupolla/leads'))

    def test_real_make_url_is_accepted(self):
        self.assertTrue(is_configured_crm_webhook('https://hook.eu2.make.com/abc123xyz456'))

    def test_http_url_is_rejected(self):
        self.assertFalse(is_configured_crm_webhook('http://hook.eu2.make.com/abc123xyz456'))


class CrmPayloadTests(SimpleTestCase):
    def test_build_lead_payload_structure(self):
        class DummyDome:
            pk = 7
            slug = 'kupolla-s'
            name = 'KUPOLLA'

        class DummyLead:
            pk = 42
            form_type = 'hero'
            name = 'Іван'
            phone = '+380501234567'
            email = 'ivan@example.com'
            country = 'Україна'
            city = 'Київ'
            message = 'Тест'
            dome_model = DummyDome()
            equipment_tier = 'standard'
            configurator_data = {'tier': 'standard', 'addons': []}
            ip_address = '127.0.0.1'
            created_at = None

            def get_form_type_display(self):
                return 'CTA Головна (hero)'

        payload = build_lead_payload(DummyLead())

        self.assertEqual(payload['id'], 42)
        self.assertEqual(payload['form_type'], 'hero')
        self.assertEqual(payload['dome_model_slug'], 'kupolla-s')
        self.assertEqual(payload['configurator_data']['tier'], 'standard')
        self.assertEqual(payload['country'], 'Україна')
        self.assertEqual(payload['city'], 'Київ')
