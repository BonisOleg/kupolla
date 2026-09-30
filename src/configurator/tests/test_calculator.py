import json

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import translation

from src.catalog.models import DomeModel
from src.configurator.models import ConfigOption
from src.configurator.utils import calculate_price, tier_delta_for


class CalculatePriceTests(TestCase):
    def setUp(self):
        translation.activate('uk')
        self.dome = DomeModel.objects.create(
            name='Test Dome',
            slug='test-dome-cfg',
            area_m2=40,
            diameter='7.5',
            height_m='4.0',
            price_base=50000,
            price_standard=60000,
            price_premium=75000,
            is_published=True,
        )
        self.addon = ConfigOption.objects.create(
            option_type=ConfigOption.OptionType.ADDON,
            code='test-addon-terrace',
            name='Тераса',
            price_delta=1500,
        )
        ConfigOption.objects.create(
            option_type=ConfigOption.OptionType.ADDON,
            code='test-addon-off',
            name='Вимкнена опція',
            price_delta=9999,
            is_active=False,
        )

    def test_tier_delta_from_dome_prices(self):
        self.assertEqual(tier_delta_for(self.dome, 'base'), 0)
        self.assertEqual(tier_delta_for(self.dome, 'standard'), 10000)
        self.assertEqual(tier_delta_for(self.dome, 'premium'), 25000)
        self.assertEqual(tier_delta_for(None, 'premium', fallback=700), 700)

    def test_total_base_tier_and_addons(self):
        result = calculate_price({
            'model': self.dome.slug,
            'tier': 'standard',
            'addons': ['test-addon-terrace'],
        })
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['total'], 61500.0)
        self.assertEqual([b['price'] for b in result['breakdown']], [50000.0, 10000.0, 1500.0])

    def test_addons_as_csv_string_and_unknown_or_inactive_ignored(self):
        result = calculate_price({
            'model': self.dome.slug,
            'addons': 'test-addon-terrace, no-such-addon, test-addon-off',
        })
        self.assertEqual(result['total'], 51500.0)
        self.assertEqual(len(result['breakdown']), 2)


class CalculatorViewTests(TestCase):
    def setUp(self):
        translation.activate('uk')
        self.dome = DomeModel.objects.create(
            name='API Dome',
            slug='test-dome-api',
            area_m2=30,
            diameter='6.8',
            height_m='3.6',
            price_base=42000,
            is_published=True,
        )
        self.url = reverse('configurator_calculate')

    def test_post_json_returns_total(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'model': self.dome.slug, 'tier': 'base'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['total'], 42000.0)
        self.assertEqual(payload['errors'], [])

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_csrf_is_enforced(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            self.url,
            data=json.dumps({'model': self.dome.slug}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)


class ConfiguratorPageTests(TestCase):
    def setUp(self):
        translation.activate('uk')
        DomeModel.objects.create(
            name='Page Dome',
            slug='test-dome-page',
            area_m2=30,
            diameter='6.8',
            height_m='3.6',
            price_base=42000,
            is_published=True,
        )

    def test_page_renders_with_selected_model(self):
        response = self.client.get('/uk/configurator/?model=test-dome-page')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-qa="lead-form"')
        self.assertContains(response, 'id="cfgPriceBar"')
        self.assertContains(response, 'id="cfgPreviewImg"')
        self.assertContains(response, 'kupolla-config-2.css')

    def test_unknown_model_falls_back_to_published_dome(self):
        response = self.client.get('/uk/configurator/?model=<script>')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<script>alert')
