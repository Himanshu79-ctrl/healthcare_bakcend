from rest_framework import serializers

from doctors.serializers import DoctorSerializer

from .models import PatientDoctorMapping


class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_detail = DoctorSerializer(source="doctor", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ("id", "patient", "patient_name", "doctor", "doctor_detail", "assigned_at")
        read_only_fields = ("id", "assigned_at")
        validators = []

    def validate_patient(self, patient):
        request = self.context["request"]
        if patient.created_by_id != request.user.id:
            raise serializers.ValidationError("Patient not found.")
        return patient

    def validate(self, attrs):
        exists = PatientDoctorMapping.objects.filter(
            patient=attrs["patient"], doctor=attrs["doctor"]
        ).exists()
        if exists:
            raise serializers.ValidationError("This doctor is already assigned to the patient.")
        return attrs
