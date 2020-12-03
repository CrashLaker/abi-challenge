from django.db import models
from map.models import Location
from django.core.validators import MaxValueValidator, MinValueValidator

class Order(models.Model):
    store = models.CharField(max_length=255)
    location = models.ForeignKey(Location,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[
                                        MaxValueValidator(50),
                                        MinValueValidator(1),
                                   ],
                                   null=False)
    def __str__(self):
        return f"{self.store} {self.quantity}"
