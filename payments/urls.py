from django.urls import path
from .views import PaymentVerifierView

urlpatterns = [path('verify/', PaymentVerifierView.as_view(), name='payment-verify')]