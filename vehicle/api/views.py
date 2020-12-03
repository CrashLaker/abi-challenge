from rest_framework import generics, mixins, viewsets
from rest_framework.exceptions import ValidationError
from vehicle.models import VehicleType, Vehicle
from vehicle.api.serializers import VehicleTypeSerializer, VehicleSerializer

class VehicleTypeAPIView(viewsets.ModelViewSet):

    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer

class VehicleAPIView(viewsets.ModelViewSet):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
