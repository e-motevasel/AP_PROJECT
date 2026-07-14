from django.db import models
from django.conf import settings
from villas.models import Villa

class Reservation(models.Model):
    STATUS = [('pending_payment','Pending Payment'), ('confirmed','Confirmed'),
            ('failed', 'Failed'), ('cancelled', 'Cancelled')]
    
    villa = models.ForeignKey(Villa,on_delete=models.CASCADE,related_name='reservations')
    
    guest = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='reservations')
    
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending_payment')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()

    def __str__(self):
        return f"Reservation: {self.id} - {self.villa.title} ({self.status})"
