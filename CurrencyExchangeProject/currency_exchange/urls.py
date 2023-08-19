from django.urls import path
from .views import ShowExchangeRatesView

urlpatterns = [
    path('show_rates/', ShowExchangeRatesView.as_view(), name='show_rates'),
]
