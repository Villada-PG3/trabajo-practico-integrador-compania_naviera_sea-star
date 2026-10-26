from django.test import TestCase
from django.urls import reverse


class PageNavigationTests(TestCase):
    def test_main_navigation_pages_load(self):
        for page in ("home", "navios", "itinerarios", "cruceros"):
            with self.subTest(page=page):
                response = self.client.get(reverse(page))
                self.assertEqual(response.status_code, 200)
