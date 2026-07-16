from django.urls import path
from .views import ReservationListCreateView, VillaReservationsView

urlpatterns = [path('', ReservationListCreateView.as_view(), name='reservation-list-create'),
               path('villa/<int:villa_id>/', VillaReservationsView.as_view(), name='villa-reservations')]