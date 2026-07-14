from rest_framework import serializers
from .models import Villa

class VillaSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Villa
        fields = ['id', 'host', 'title', 'city', 'address', 'price_per_night', 'capacity', 'amenities']
        read_only_fields = ['host']