from django.db import models
from reservations.models import Reservation

class Payment(models.Model):

    STATUS = [('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')]
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    gateway_ref = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.id} for {self.reservation_id} ({self.status})"
