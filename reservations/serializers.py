from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Reservation
        fields = ['id', 'guest', 'villa', 'check_in', 'check_out', 'status', 'created_at', 'total_price']
        read_only_fields = ['guest', 'status', 'created_at', 'total_price']

