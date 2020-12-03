from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from order.api.serializers import OrderSerializer, ScoreSerializer
from map.api.serializers import MapSerializer
from order.models import Order
from vehicle.models import Vehicle
from map.models import Map
from rest_framework.views import APIView
from core.algo import Algo

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ScoreViewSet(APIView):
    #queryset = Vehicle.objects.all()
    serializer_class = ScoreSerializer
    
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        graph = [
            {
                "source":   m.source.name,
                "target":   m.target.name,
                "distance": m.distance
            }
            for m in Map.objects.all()
        ]
        vehicles = [
            {
                "id_vehicle": v.id,
                "model":      v.model,
                "location":   v.location.name,
                "capacity":   v.vehicle_type.cargo_capacity,
            }
            for v in Vehicle.objects.all()
        ]
        order = {
            "name": order.store,
            "quantity": order.quantity,
            "location": order.location.name
        }
        print(graph)
        print(vehicles)
        print(order)
        vechiles = Algo(graph, vehicles, order) \
                        .boilerplate() \
                        .get_score_list()
        #vehicles2 = [{"model": "F1000", "cargo_capacity": 40, "location": "B", "score": 87.5}, {"model": "F1000", "cargo_capacity": 20, "location": "C", "score": 62.5}, {"model": "F1000", "cargo_capacity": 20, "location": "E", "score": 50.0}]

        return Response(vehicles, status=status.HTTP_200_OK)
