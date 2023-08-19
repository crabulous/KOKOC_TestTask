# currency_exchange/management/commands/update_exchange_rates.py

import requests
from django.core.management.base import BaseCommand
from currency_exchange.models import Currency, ExchangeRate
from datetime import datetime


class Command(BaseCommand):
    help = 'Update exchange rates from the provided URL'

    def handle(self, *args, **options):
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        data = response.json()

        date = datetime.strptime(data['Date'], '%Y-%m-%dT%H:%M:%S%z').date()

        for char_code, currency_data in data['Valute'].items():
            name = currency_data['Name']
            value = currency_data['Value']

            currency, _ = Currency.objects.get_or_create(char_code=char_code, defaults={'name': name})
            exchange_rate, created = ExchangeRate.objects.get_or_create(currency=currency, date=date,
                                                                        defaults={'value': value})

            if not created:
                exchange_rate.value = value
                exchange_rate.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated exchange rate for {currency} on {date}: {value}'))
