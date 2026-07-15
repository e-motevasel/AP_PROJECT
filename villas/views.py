from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Villa
from .serializers import VillaSerializer
from .permissions import IsHost

from .serializers import AvailabilitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Availability


class VillaListCreateView(generics.ListCreateAPIView):

    serializer_class = VillaSerializer

    def get_queryset(self):

        queryset = Villa.objects.all()
        city = self.request.query_params.get('city')

        if city:

            queryset = queryset.filter(city__iexact=city)
        
        return queryset
    
    def get_permissions(self):
        
        if self.request.method == 'POST':

            return [permissions.IsAuthenticated(), IsHost()]
        
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        
        serializer.save(host=self.request.user)

class VillaDetailView(generics.RetrieveAPIView):

    queryset = Villa.objects.all()
    serializer_class = VillaSerializer
    permission_classes = [permissions.IsAuthenticated]






class AvailabilityCreateView(APIView):

    permission_classes = [permissions.IsAuthenticated, IsHost]

    def post(self, request, villa_id):

        try:
            villa = Villa.objects.get(id = villa_id)

        except (Villa.DoesNotExist):
            return Response({'detail': 'Villa not found.'}, status= status.HTTP_404_NOT_FOUND)
        
        if(villa.host != request.user):
            return Response({'detail': 'You can\'t manage availability for others villas.'}, status=status.HTTP_403_FORBIDDEN)

        dates = request.data.get('dates', [])

        if(len(dates) == 0):
            return Response({'detail': 'dates list required.'}, status=status.HTTP_400_BAD_REQUEST)

        listt = []

        for date in dates:
            availability, exist = Availability.objects.get_or_create(villa = villa, date = date, defaults={'is_available': True})
            listt.append(availability)

        serializer = AvailabilitySerializer(listt, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
