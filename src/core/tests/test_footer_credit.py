from django.test import TestCase
from django.urls import reverse

CREDIT_URL = 'https://www.prometeylabs.com/corporate-website-v2/'


class FooterDeveloperLinkTests(TestCase):
    def test_home_has_nofollow_credit_link(self):
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, CREDIT_URL)
        self.assertContains(response, 'nofollow')
        self.assertContains(response, '>PrometeyLabs</a>')

    def test_localized_home_keeps_credit_link(self):
        for path in ('/', '/en/'):
            response = self.client.get(path)
            self.assertContains(response, CREDIT_URL)

    def test_inner_pages_show_credit_without_link(self):
        for url in (reverse('about:index'), reverse('contacts:index')):
            response = self.client.get(url)
            self.assertContains(response, 'PrometeyLabs')
            self.assertNotContains(response, CREDIT_URL)
            self.assertNotContains(response, 'kp-devcredit__brand" href')
