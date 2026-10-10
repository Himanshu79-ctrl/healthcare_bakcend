from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from doctors.models import Doctor
from patients.models import Patient

from .models import PatientDoctorMapping

User = get_user_model()


class MappingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="a@example.com", email="a@example.com", password="pass12345")
        self.other = User.objects.create_user(username="b@example.com", email="b@example.com", password="pass12345")
        self.client.force_authenticate(self.user)
        self.patient = Patient.objects.create(
            created_by=self.user, name="Amit", age=30, gender="male", phone="9876543210"
        )
        self.doctor = Doctor.objects.create(
            created_by=self.user,
            name="Neha",
            email="neha@clinic.com",
            phone="9123456780",
            specialization="Cardiology",
        )

    def test_assign_doctor(self):
        response = self.client.post(
            reverse("mapping-list"),
            {"patient": self.patient.id, "doctor": self.doctor.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_assignment_rejected(self):
        data = {"patient": self.patient.id, "doctor": self.doctor.id}
        self.client.post(reverse("mapping-list"), data, format="json")
        response = self.client.post(reverse("mapping-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_assign_to_other_users_patient(self):
        foreign = Patient.objects.create(
            created_by=self.other, name="Raj", age=40, gender="male", phone="9000000000"
        )
        response = self.client.post(
            reverse("mapping-list"),
            {"patient": foreign.id, "doctor": self.doctor.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_doctors_for_patient(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        response = self.client.get(reverse("mapping-detail", args=[self.patient.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_remove_mapping(self):
        mapping = PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        response = self.client.delete(reverse("mapping-detail", args=[mapping.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PatientDoctorMapping.objects.exists())
