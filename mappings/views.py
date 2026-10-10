from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import MappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = MappingSerializer
    search_fields = ["patient__name", "doctor__name"]
    ordering_fields = ["assigned_at"]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        ).select_related("patient", "doctor")


class MappingDetailView(APIView):
    @extend_schema(responses=MappingSerializer(many=True))
    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        mappings = PatientDoctorMapping.objects.filter(patient=patient).select_related(
            "patient", "doctor"
        )
        serializer = MappingSerializer(mappings, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(responses={204: None})
    def delete(self, request, pk):
        mapping = get_object_or_404(
            PatientDoctorMapping, pk=pk, patient__created_by=request.user
        )
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
