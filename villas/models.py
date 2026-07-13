from django.conf import settings
from django.db import models


class Villa(models.Model):

    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='villas')
    title = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.TextField()
    price_per_night = models.IntegerField()
    capacity = models.PositiveIntegerField()
    amenities = models.JSONField(default=list, blank=True)


class Availability(models.Model):

    villa = models.ForeignKey(Villa, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('villa', 'date')