from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Doctor
from .permissions import IsCreatorOrReadOnly
from .serializers import DoctorSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    search_fields = ["name", "specialization", "email"]
    ordering_fields = ["name", "experience_years", "created_at"]

    def get_queryset(self):
        queryset = Doctor.objects.all()
        specialization = self.request.query_params.get("specialization")
        if specialization:
            queryset = queryset.filter(specialization__iexact=specialization)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
