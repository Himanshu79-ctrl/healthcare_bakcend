from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Doctor

User = get_user_model()


class DoctorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="a@example.com", email="a@example.com", password="pass12345")
        self.other = User.objects.create_user(username="b@example.com", email="b@example.com", password="pass12345")
        self.client.force_authenticate(self.user)
        self.payload = {
            "name": "Neha Verma",
            "email": "neha@clinic.com",
            "phone": "9123456780",
            "specialization": "Cardiology",
            "experience_years": 8,
        }

    def test_create_doctor(self):
        response = self.client.post(reverse("doctor-list"), self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_email_rejected(self):
        self.client.post(reverse("doctor-list"), self.payload, format="json")
        response = self.client.post(reverse("doctor-list"), self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_everyone_can_list_doctors(self):
        Doctor.objects.create(created_by=self.other, **self.payload)
        response = self.client.get(reverse("doctor-list"))
        self.assertEqual(len(response.data["results"]), 1)

    def test_only_creator_can_modify(self):
        doctor = Doctor.objects.create(created_by=self.other, **self.payload)
        url = reverse("doctor-detail", args=[doctor.id])
        self.assertEqual(self.client.put(url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_specialization(self):
        Doctor.objects.create(created_by=self.user, **self.payload)
        other = {**self.payload, "email": "raj@clinic.com", "specialization": "Neurology"}
        Doctor.objects.create(created_by=self.user, **other)
        response = self.client.get(reverse("doctor-list"), {"specialization": "neurology"})
        self.assertEqual(len(response.data["results"]), 1)
