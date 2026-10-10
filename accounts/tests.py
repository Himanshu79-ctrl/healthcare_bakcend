from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.payload = {
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
            "password": "StrongPass@123",
        }

    def test_register_success(self):
        response = self.client.post(self.register_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)

    def test_register_duplicate_email(self):
        self.client.post(self.register_url, self.payload, format="json")
        response = self.client.post(self.register_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_weak_password(self):
        self.payload["password"] = "12345678"
        response = self.client.post(self.register_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_tokens(self):
        self.client.post(self.register_url, self.payload, format="json")
        response = self.client.post(
            self.login_url,
            {"email": self.payload["email"], "password": self.payload["password"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        self.client.post(self.register_url, self.payload, format="json")
        response = self.client.post(
            self.login_url,
            {"email": self.payload["email"], "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        self.client.post(self.register_url, self.payload, format="json")
        login = self.client.post(
            self.login_url,
            {"email": self.payload["email"], "password": self.payload["password"]},
            format="json",
        )
        response = self.client.post(
            reverse("token-refresh"), {"refresh": login.data["refresh"]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
