from django.shortcuts import render
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from villas.models import Availability
from reservations.models import Reservation
from .models import Payment
from .serializers import PaymentSerializer


class PaymentVerifierView(generics.GenericAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, *args, **kwargs):

        reservation_id = request.data.get('reservation')
        success = request.data.get('success')

        if not reservation_id or success == None:

            return Response(
                {'detail': 'reservation and success are needed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            reservation = Reservation.objects.get(id=reservation_id)

        except Reservation.DoesNotExist:

            return Response(
                {'detail': 'Reservation not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if reservation.guest != request.user:

            return Response(
                {'detail': 'This reservation is not yours.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if reservation.status != 'pending_payment':

            return Response(
                {'detail': 'This reservation is not in pending payment status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():

            payment = Payment()
            payment.reservation = reservation
            payment.amount = reservation.total_price

            if success == True:

                payment.status = 'success'
                payment.save()

                reservation.status = 'confirmed'
                reservation.save()
            
            else:

                payment.status = 'failed'
                payment.save()

                reservation.status = 'failed'
                reservation.save()

                availibility_list = Availability.objects.select_for_update().filter(
                    villa = reservation.villa,
                    date__gte=reservation.check_in,
                    date__lt=reservation.check_out
                )
                availibility_list.update(is_available=True)

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)    