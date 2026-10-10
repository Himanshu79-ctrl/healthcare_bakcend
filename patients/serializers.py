from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "name",
            "age",
            "gender",
            "phone",
            "address",
            "medical_history",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_age(self, value):
        if value < 0 or value > 130:
            raise serializers.ValidationError("Age must be between 0 and 130.")
        return value

    def validate_phone(self, value):
        digits = value.replace("+", "").replace(" ", "").replace("-", "")
        if not digits.isdigit() or not 7 <= len(digits) <= 15:
            raise serializers.ValidationError("Enter a valid phone number.")
        return value
