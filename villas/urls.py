from django.urls import path
from .views import VillaDetailView, VillaListCreateView

urlpatterns = [path('', VillaListCreateView.as_view(), name='villa-list-create'),
               path('<int:pk>/', VillaDetailView.as_view(), name='villa-detail')]

