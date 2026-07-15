from rest_framework import serializers
from .models import Villa, Availability

class VillaSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Villa
        fields = ['id', 'host', 'title', 'city', 'address', 'price_per_night', 'capacity', 'amenities']
        read_only_fields = ['host']



class AvailabilitySerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Availability
        fields = ['id', 'villa', 'date', 'is_available']
        read_only_fields = ['villa']
        