from rest_framework import serializers
from order.models import Order
from vehicle.models import Vehicle

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = "__all__"

class ScoreSerializer(serializers.ModelSerializer):
    id_vehicle = serializers.SerializerMethodField()
    model      = serializers.SerializerMethodField()
    location   = serializers.SerializerMethodField()
    capacity   = serializers.SerializerMethodField()
    score      = serializers.SerializerMethodField()
    
    class Meta:
        model = Vehicle 
        fields = ("id_vehicle", "model", "location", "capacity", "score")

    def get_id_vehicle(self, instance):
        return instance.id
    
    def get_model(self, instance):
        return instance.model

    def get_location(self, instance):
        return instance.location.name

    def get_capacity(self, instance):
        return instance.vehicle_type.cargo_capacity

    def get_score(self, instance):
        return 0
