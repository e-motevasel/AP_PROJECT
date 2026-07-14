from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from .views import RegisterView

urlpatterns = [path('register/', RegisterView.as_view(), name='register'), 
               path('login/', ObtainAuthToken.as_view(), name='login')
               ]