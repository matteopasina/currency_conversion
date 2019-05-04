from rates_retriever import RateRetriever
from data.constants import *
from decimal import Decimal
from datetime import datetime


class CurrencyConverter:
    def __init__(self, from_currency, to_currency, value):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.value = Decimal(value.replace(',', '.'))
        self.retriever = RateRetriever(RATES_FILE)
        self.response = {}

    def convert(self):
        self.retriever.load_rates()

        conversion_rate = self._compute_conversion_rate()
        converted_value = self.value * conversion_rate

        self._build_response(converted_value, conversion_rate)

        return self.response

    def _build_response(self, converted_value, conversion_rate):
        self.response['converted_value'] = str(converted_value.quantize(Decimal('.0001')))
        self.response['from_currency'] = self.from_currency
        self.response['to_currency'] = self.to_currency
        self.response['original_value'] = str(self.value)
        self.response['conversion_rate'] = str(conversion_rate.quantize(Decimal('.0001')))
        self.response['timestamp'] = datetime.now().isoformat()

    def _compute_conversion_rate(self):
        # If from USD
        if self.from_currency == self.retriever.conversion_rates['base']:
            return Decimal(self.retriever.conversion_rates['rates'][self.to_currency])

        # If to USD
        elif self.to_currency == self.retriever.conversion_rates['base']:
            return Decimal(1 / self.retriever.conversion_rates['rates'][self.from_currency])

        # Other cases
        else:
            rate_from = Decimal(self.retriever.conversion_rates['rates'][self.from_currency])
            rate_to = Decimal(self.retriever.conversion_rates['rates'][self.to_currency])
            return rate_to/rate_from


