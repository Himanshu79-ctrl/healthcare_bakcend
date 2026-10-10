from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Patient

User = get_user_model()


class PatientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="a@example.com", email="a@example.com", password="pass12345")
        self.other = User.objects.create_user(username="b@example.com", email="b@example.com", password="pass12345")
        self.client.force_authenticate(self.user)
        self.payload = {"name": "Amit", "age": 34, "gender": "male", "phone": "9876543210"}

    def test_requires_authentication(self):
        self.client.force_authenticate(None)
        response = self.client.get(reverse("patient-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_patient(self):
        response = self.client.post(reverse("patient-list"), self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.get().created_by, self.user)

    def test_invalid_phone(self):
        self.payload["phone"] = "abc"
        response = self.client.post(reverse("patient-list"), self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_own_patients(self):
        Patient.objects.create(created_by=self.other, **self.payload)
        Patient.objects.create(created_by=self.user, **self.payload)
        response = self.client.get(reverse("patient-list"))
        self.assertEqual(len(response.data), 1)

    def test_cannot_access_other_users_patient(self):
        patient = Patient.objects.create(created_by=self.other, **self.payload)
        response = self.client.get(reverse("patient-detail", args=[patient.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_and_delete(self):
        patient = Patient.objects.create(created_by=self.user, **self.payload)
        url = reverse("patient-detail", args=[patient.id])
        self.payload["age"] = 40
        response = self.client.put(url, self.payload, format="json")
        self.assertEqual(response.data["age"], 40)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
