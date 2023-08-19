from django.shortcuts import render
from django.views import View
from .models import ExchangeRate
from datetime import datetime
from django.core.management import call_command


class ShowExchangeRatesView(View):
    template_name = 'exchange_rates.html'

    def get(self, request, *args, **kwargs):
        date_str = request.GET.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        exchange_rates = ExchangeRate.objects.filter(date=date)

        if not exchange_rates.exists():
            call_command('update_exchange_rates')

        exchange_rates = ExchangeRate.objects.filter(date=date)

        context = {
            'date': date,
            'exchange_rates': exchange_rates
        }
        return render(request, self.template_name, context)
