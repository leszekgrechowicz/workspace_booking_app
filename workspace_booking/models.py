from django.db import models


# Create your models here.

class Office(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_capacity = models.SmallIntegerField()
    projector_available = models.BooleanField(default=False)


