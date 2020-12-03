from rest_framework import generics, mixins, viewsets
from rest_framework.exceptions import ValidationError
from map.models import Location, Map
from map.api.serializers import (LocationSerializer,
                                 MapSerializer,
                                 MapListSerializer)

class LocationViewSet(viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def perform_create(self, serializer):
        serializer.save()

class MapViewSet(viewsets.ModelViewSet):

    queryset = Map.objects.all()
    serializer_class = MapSerializer

    def perform_create(self, serializer):
        if serializer.validated_data['source'] == serializer.validated_data['target']:
            raise ValidationError('Source cannot be the same as target')

        count_st = Map.objects.filter(
            source=serializer.validated_data['source'],
            target=serializer.validated_data['target']
        ).count() >= 1
        count_ts = Map.objects.filter(
            source=serializer.validated_data['target'],
            target=serializer.validated_data['source']
        ).count() >= 1
        if count_st or count_ts:
            raise ValidationError('There already exists an entry with such '
                                  'source and destination or vice versa '
                                  'added')

        serializer.save()

class MapListAPIView(mixins.ListModelMixin,
                     generics.GenericAPIView):

    queryset = Map.objects.all()
    serializer_class = MapListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

