import json

from django.core.urlresolvers import reverse
from django.test import TestCase


class UserLocationViewTest(TestCase):
    def setUp(self):
        url = reverse("users-location-add")
        data = {'lat': 123.12, 'lon': 38.24}
        self.response = self.client.post(url, data)

    def test_add_location(self):
        # any location that can be parsed into a number is considered valid.
        json_response = json.loads(self.response.content.decode('utf-8'))
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(json_response['status'], 'success')

    def test_remove_location(self):
        # users sure be able to clear their location as well
        url = reverse("users-location-remove")
        response = self.client.post(url)
        json_response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'success')
