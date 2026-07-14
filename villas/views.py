from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Villa
from .serializers import VillaSerializer
from .permissions import IsHost

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


