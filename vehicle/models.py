from django.db import models
from map.models import Location

class VehicleType(models.Model):
    name = models.CharField(max_length=10, unique=True)
    cargo_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.cargo_capacity}"

class Vehicle(models.Model):
    model = models.CharField(max_length=255, null=False)
    location = models.ForeignKey(Location,
                                 on_delete=models.CASCADE,
                                 null=False)
    vehicle_type = models.ForeignKey(VehicleType,
                                     on_delete=models.CASCADE)

    def __str__(self):
        return (f"Model:{self.model} "
                f"Loc:{self.location.name} "
                f"Type:{self.vehicle_type.name}")

