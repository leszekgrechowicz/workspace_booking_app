from django.db import models

# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_capacity = models.PositiveSmallIntegerField()
    projector_available = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_name}"


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)
    company_name = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('room', 'date')






