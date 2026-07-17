from django.shortcuts import render
from datetime import date as date_class
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from villas.models import Villa, Availability
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationListCreateView(generics.ListCreateAPIView):

    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(guest=self.request.user)
    
    def create(self, request, *args, **kwargs):

        villa_id = request.data.get('villa_id')
        check_in_string = request.data.get('check_in')
        check_out_str = request.data.get('check_out')

        if not villa_id or not check_in_string or not check_out_str:

            return Response(
                {'detail': 'villa, check_in and check_out needed.'},
                status=status.HTTP_400_BAD_REQUEST

            )
        
        try:
            
            villa = Villa.objects.get(id=villa_id)

        except Villa.DoesNotExist:

            return Response(
                {'detail': 'Villa not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        check_in_date = date_class.fromisoformat(check_in_string)
        check_out_date = date_class.fromisoformat(check_out_str)

        if check_out_date <= check_in_date:

            return Response(
                {'detail': 'check_out must be after check_in'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        nights = (check_out_date - check_in_date).days

        with transaction.atomic():

            availability_list = Availability.objects.select_for_update().filter(villa=villa, date__gte=check_in_date, date__lt=check_out_date)

            available_count = availability_list.filter(is_available=True).count()

            if available_count != nights:

                return Response(
                    {'detail': 'Desired Dates are unavailable'},
                    status=status.HTTP_409_CONFLICT
                )
            
            total_price = nights * villa.price_per_night
            
            reservation = Reservation.objects.create(
                guest=request.user,
                villa=villa,
                check_in=check_in_date,
                check_out=check_out_date,
                total_price=total_price,
                status='pending_payment'
            )

            availability_list.update(is_available=False)
    
        serializer = self.get_serializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class VillaReservationsView(generics.ListAPIView):

    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        villa_id = self.kwargs.get('villa_id')

        try:
            villa = Villa.objects.get(id = villa_id)
        
        except (Villa.DoesNotExist):
            return Reservation.objects.none()

        if(villa.host != self.request.user):
            return Reservation.objects.none()
        
        return Reservation.objects.filter(villa = villa)