from rest_framework import serializers
from map.models import Location, Map

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"

class MapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Map 
        fields = "__all__"

class MapListSerializer(serializers.ModelSerializer):

    source = serializers.StringRelatedField()
    target = serializers.StringRelatedField()

    class Meta:
        model = Map 
        fields = "__all__"
