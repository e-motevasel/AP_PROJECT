from django.urls import path
from .views import VillaDetailView, VillaListCreateView, AvailabilityCreateView

urlpatterns = [path('', VillaListCreateView.as_view(), name='villa-list-create'),
               path('<int:pk>/', VillaDetailView.as_view(), name='villa-detail'),
               path('<int:villa_id>/availability/', AvailabilityCreateView.as_view(), name='availability-create')]
