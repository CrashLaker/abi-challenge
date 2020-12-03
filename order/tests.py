from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from pprint import pprint

class TestRanking(TestCase):

    def setUp(self):
        self.client = APIClient()


    def test_problemset1(self):

        # insert locations
        locations = "ABCDEF"
        location_cache = {}
        print("+ Insert location")
        for loc in locations:
            payload = {"name": loc}
            rs = self.client.post("/v1/locations/", payload)
            print(rs.json())
            location_cache[loc] = rs.json()["id"]
        
        
        graph = [
            {"source": "A", "target": "B", "distance": 5},
            {"source": "B", "target": "C", "distance": 7},
            {"source": "B", "target": "D", "distance": 3},
            {"source": "C", "target": "E", "distance": 4},
            {"source": "D", "target": "E", "distance": 10},
            {"source": "D", "target": "F", "distance": 8},
        ]
        
        # insert mapping A->B distance 5
        print("+ Insert mapping")
        for g in graph:
            g["source"] = location_cache[g["source"]]
            g["target"] = location_cache[g["target"]]
            payload = g
            rs = self.client.post("/v1/locations-map/", payload)
            print(rs.json())
    
        
        # insert vehicles-types
        vehicles_types = [
            {"name": "A", "cargo_capacity": 10},
            {"name": "B", "cargo_capacity": 20},
            {"name": "C", "cargo_capacity": 30},
            {"name": "D", "cargo_capacity": 40},
            {"name": "E", "cargo_capacity": 50},
        ]
        vehicles_types_cache = {} 
        for v in vehicles_types:
            payload = v
            rs = self.client.post("/v1/vehicle-types/", payload)
            print(rs.json())
            vehicles_types_cache[v["name"]] = rs.json()["id"]


        # insert vehicles
        print("+ Insert vehicles")
        vehicles = [
            {"model": "F1000", "vehicle_type": "D", "location": "B"},
            {"model": "F1000", "vehicle_type": "B", "location": "C"},
            {"model": "F1000", "vehicle_type": "B", "location": "E"},
        ]
        for v in vehicles:
            v["location"] = location_cache[v["location"]]
            v["vehicle_type"] = vehicles_types_cache[v["vehicle_type"]]
            payload = v
            rs = self.client.post("/v1/vehicle/", payload)
            print(rs.json())

        
        # insert order
        print("+ Insert order")
        payload = {
            "store": "Empório da Cerveja",
            "location": location_cache["A"],
            "quantity": 30
        }
        rs = self.client.post("/v1/order/", payload)
        print(rs.json())
        order = rs.json()

        
        print("Get vehicle score ranking")
        rs = self.client.get(f"/v1/order/{order['id']}/vehicle/ranking")
        pprint(rs.json())
        

        result = [
          {
            "id_vehicle": 1,
            "model": "F1000",
            "location": "B",
            "capacity": 40,
            "score": 87.5
          },
          {
            "id_vehicle": 2,
            "model": "F1000",
            "location": "C",
            "capacity": 20,
            "score": 62.5
          },
          {
            "id_vehicle": 3,
            "model": "F1000",
            "location": "E",
            "capacity": 20,
            "score": 50
          }
        ]

        self.assertEqual(result, rs.json())



















