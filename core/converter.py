from data.constants import *
from decimal import Decimal
from datetime import datetime
PRECISION = Decimal('.0001')


class CurrencyConverter:
    """
    This class converts a value from a currency to another
    """

    def __init__(self, from_currency, to_currency, value, retriever):
        """
        :param from_currency: the original currency of the value
        :param to_currency: the desired currency
        :param value: the value to be converted
        :param retriever: the retriever object that is uses to get the exchange rates
        """
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.response = {}
        self.value = value
        self.retriever = retriever
        self.conversion_rate = None

    def convert(self):
        """
        This method checks if the currencies are supported, then loads the latest rates and computes the conversion
        :return: the converted value
        """

        # Currencies supported are USD, EUR, PLN, CZK
        if self.from_currency not in CURRENCIES_SUPPORTED or self.to_currency not in CURRENCIES_SUPPORTED:
            self.response['ERROR'] = "Currency not supported"
            return self.response

        try:
            self.value = Decimal(self.value.replace(',', '.'))
        except Exception as e:
            print(e)
            self.response['ERROR'] = "Not a valid value to convert"
            return self.response

        if not self.retriever.conversion_rates:
            self.retriever.load_rates()

        base = self.retriever.conversion_rates['base']
        rates = self.retriever.conversion_rates['rates']

        self.conversion_rate = self._compute_conversion_rate(base, rates)
        converted_value = self.value * self.conversion_rate

        return converted_value

    def build_response(self, converted_value):
        """
        This method builds the dictionary with the converted value and some information about the conversion
        :param converted_value: the converted value
        :return: a dict with all the information of the conversion that can be sent as a response to the client
        """
        if 'ERROR' in self.response:
            return self.response
        self.response['converted_value'] = str(converted_value.quantize(PRECISION))
        self.response['from_currency'] = self.from_currency
        self.response['to_currency'] = self.to_currency
        self.response['original_value'] = str(self.value)
        self.response['conversion_rate'] = str(self.conversion_rate.quantize(PRECISION))
        self.response['timestamp'] = datetime.now().isoformat()
        return self.response

    def _compute_conversion_rate(self, base, rates):
        """
        This method computes the conversion rate of the conversion, since the free API returns only the rates
        for USD as base, the other conversion rates have to be computed from that
        :param base: the base currency
        :param rates: the rates available
        :return: the conversion rate as Decimal
        """
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


