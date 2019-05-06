from core.converter import CurrencyConverter


class MultiCurrencyConverter(CurrencyConverter):
    """
    This class handles the conversion of multiple values from multiple currencies
    """

    def __init__(self, retriever):
        """
        :param retriever: the retriever object that is uses to get the exchange rates
        """
        self.from_currency = None
        self.to_currency = None
        self.value = None
        self.retriever = retriever
        self.response = {}

    def multi_convert(self, request):
        """
        Given the POST request received this method computes the converted values using the convert method
        of CurrencyConverter and builds the response
        :param request: json body of the POST request
        :return: the response that can be sent to the client
        """
        converted_amounts_obj = []

        self.to_currency = request['to_currency']

        self.response['to_currency'] = self.to_currency

        for amount_currency in request['amounts']:
            amount_obj = dict()
            conv_amounts = []

            self.from_currency = amount_currency['from_currency']
            amount_obj['from_currency'] = self.from_currency

            for amount in amount_currency['amounts']:
                self.value = amount
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
