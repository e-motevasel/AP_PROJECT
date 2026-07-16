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

from datetime import date

class VillaListCreateView(generics.ListCreateAPIView):

    serializer_class = VillaSerializer

    def get_queryset(self):

        queryset = Villa.objects.all()
        city = self.request.query_params.get('city')

        if city:

            queryset = queryset.filter(city__iexact=city)

        strcheck_in = self.request.query_params.get('check_in')
        strcheck_out = self.request.query_params.get('check_out')

        if(strcheck_in and strcheck_out):

            date_in = date.fromisoformat(strcheck_in)
            date_out = date.fromisoformat(strcheck_out)

            nights = (date_out - date_in).days

            id_avail_villa = []

            for villa in queryset:

                avail_days = Availability.objects.filter(villa = villa, date__gte = date_in, date__lt = date_out, is_available = True).count()

                if(avail_days == nights):
                    id_avail_villa.append(villa.id)

            queryset = queryset.filter(id__in = id_avail_villa)



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
