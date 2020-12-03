from django.db import models



class Location(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Map(models.Model):
    source = models.ForeignKey(Location,
                               on_delete=models.CASCADE)
    target = models.ForeignKey(Location,
                               on_delete=models.CASCADE,
                               related_name='%(class)s_target')
    distance = models.FloatField()

    def __str__(self):
        return f"{self.source.name} to {self.target.name} = {self.distance}"


