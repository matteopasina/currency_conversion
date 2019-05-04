from data.constants import *
from decimal import Decimal
from datetime import datetime
PRECISION = Decimal('.0001')


class CurrencyConverter:

    def __init__(self, from_currency, to_currency, value, retriever):
        self.from_currency = from_currency
        self.to_currency = to_currency
        if value:
            self.value = Decimal(value.replace(',', '.'))
        self.retriever = retriever
        self.response = {}

    def convert(self):
        if self.from_currency not in CURRENCIES_SUPPORTED or self.to_currency not in CURRENCIES_SUPPORTED:
            self.response['ERROR'] = "Currency not supported"
            return self.response

        if not self.retriever.conversion_rates:
            self.retriever.load_rates()

        base = self.retriever.conversion_rates['base']
        rates = self.retriever.conversion_rates['rates']

        conversion_rate = self._compute_conversion_rate(base, rates)
        converted_value = self.value * conversion_rate

        return converted_value

    def build_response(self, converted_value, conversion_rate):
        self.response['converted_value'] = str(converted_value.quantize(PRECISION))
        self.response['from_currency'] = self.from_currency
        self.response['to_currency'] = self.to_currency
        self.response['original_value'] = str(self.value)
        self.response['conversion_rate'] = str(conversion_rate.quantize(PRECISION))
        self.response['timestamp'] = datetime.now().isoformat()
        return self.response

    def _compute_conversion_rate(self, base, rates):
        # If from USD
        if self.from_currency == base:
            return Decimal(rates[self.to_currency]).quantize(PRECISION)

        # If to USD
        elif self.to_currency == base:
            return Decimal(1 / rates[self.from_currency]).quantize(PRECISION)

        # Other cases
        else:
            rate_from = Decimal(rates[self.from_currency])
            rate_to = Decimal(rates[self.to_currency])
            return (rate_to/rate_from).quantize(PRECISION)


