from rest_framework import generics

from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    search_fields = ["name", "phone"]
    ordering_fields = ["name", "age", "created_at"]

    def get_queryset(self):
        queryset = Patient.objects.filter(created_by=self.request.user)
        gender = self.request.query_params.get("gender")
        if gender:
            queryset = queryset.filter(gender=gender.lower())
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
