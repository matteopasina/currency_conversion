from core.converter import CurrencyConverter
from decimal import Decimal


class MultiCurrencyConverter(CurrencyConverter):

    def __init__(self, retriever):
        self.from_currency = None
        self.to_currency = None
        self.value = None
        self.retriever = retriever
        self.response = {}

    def multi_convert(self, request):
        converted_amounts_obj = []

        self.to_currency = request['to_currency']

        self.response['to_currency'] = self.to_currency

        for amount_currency in request['amounts']:
            amount_obj = dict()
            conv_amounts = []

            self.from_currency = amount_currency['from_currency']
            amount_obj['from_currency'] = self.from_currency

            for amount in amount_currency['amounts']:
                self.value = Decimal(amount.replace(',', '.'))
                if conv_amounts:
                    conv_amounts.append(str(self.convert()))
                else:
                    conv_amounts = [str(self.convert())]

            amount_obj['converted_amounts'] = conv_amounts

            if converted_amounts_obj:
                converted_amounts_obj.append(amount_obj)
            else:
                converted_amounts_obj = [amount_obj]

        self.response['converted-amounts'] = converted_amounts_obj

        return self.response
