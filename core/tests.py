from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    def test_health_check(self):
        response = self.client.get(reverse("health-check"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["database"], "up")


class ThrottleTests(APITestCase):
    def setUp(self):
        cache.clear()

    def test_login_is_rate_limited(self):
        url = reverse("login")
        payload = {"email": "x@example.com", "password": "wrong"}
        codes = [self.client.post(url, payload, format="json").status_code for _ in range(25)]
        self.assertIn(status.HTTP_429_TOO_MANY_REQUESTS, codes)

    def test_swagger_schema_generates(self):
        response = self.client.get(reverse("schema"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
