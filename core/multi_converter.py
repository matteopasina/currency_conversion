
import re

from pyb.tracer import trace, INFO, DEBUG, ERROR
from datetime import datetime
from decimal import Decimal, getcontext
from math import ceil

from services.currency_conversion.endpoints.currency_conversion_helper import CurrencyConverterHelper
from helpers.misc.tools import time_in_range


class CurrencyConverter:

    def __init__(self):

        getcontext().prec = 7
        self.rounding_value = 0.5
        self.decimals = 2
        self.response = {'convertedAmounts': []}

        self.helper = CurrencyConverterHelper()
        self.rules = self.helper.load_rules()['rules']

    def select_rule(self, pos, distributor, to_currency, dict_provider):
        """
        This function checks if there is a rule for the conversion and in the positive case it returns the rate
        of the conversion
        :param pos: point of sale (OfficeID)
        :param distributor: Distributor
        :param to_currency: Currency to which we convert
        :param dict_provider: Dictionary with all the amounts for a single provider
        :return: rate with rate decimal places or warning if no conversion rate found
        """
        trace(INFO, "Selecting rule")
        for rule in self.rules:
            if re.match(rule['pos'], pos) and \
                    re.match(rule['distributor'], distributor) and \
                    re.match(rule['provider'], dict_provider['provider'].split('/')[0]) and \
                    dict_provider['fromCurrency'] == rule['from_currency'] and \
                    to_currency == rule['to_currency']:

                trace(INFO, "Selected rule {}".format(rule))
                start_selling_date = datetime.strptime(rule['start_selling_date'], '%d %B %Y')
                end_selling_date = datetime.strptime(rule['end_selling_date'], '%d %B %Y')
                if time_in_range(start_selling_date, end_selling_date, datetime.today()):
                    return [rule['rate'], rule['rate_decimal_places']]
                else:
                    trace(INFO, "Rule not in current time range")
        return "No rule found"

    def convert_hard_rounding(self, amounts, rate, amount_decimal_places):
        """
        This function returns a dictionary of converted amounts given a dictionary of amounts and a conversion rate
        The rounding rule rounds up to the next integer: 54,14 -> 55,00
        :param amounts: List with all the amounts to convert
        :param rate: conversion rate
        :param amount_decimal_places: decimal places of all the amounts
        :return: list containing the converted amounts
        """

        trace(INFO, "Converting")
        converted_amounts = []
        for amount in amounts:

            amount_value = int(amount) / Decimal(10 ** int(amount_decimal_places))
            converted_amount_value = amount_value * rate

            converted_amount_value = ceil(converted_amount_value) * 100

            str_converted_amount_value = str(converted_amount_value)

            if len(str_converted_amount_value) == 1:
                str_converted_amount_value = "{}{}".format("00", str_converted_amount_value)

            elif len(str_converted_amount_value) == 2:
                str_converted_amount_value = "{}{}".format("0", str_converted_amount_value)

            converted_amounts.append(str_converted_amount_value)

        return converted_amounts

    def convert_soft_rounding(self, amounts, rate, amount_decimal_places):
        """
        ***CURRENTLY NOT USED***
        This function returns a dictionary of converted amounts given a dictionary of amounts and a conversion rate
        The rounding rule rounds to the first decimal place: 54,14 -> 54,10 | 54, 15 -> 54,15 | 54, 16 -> 54,20
        :param amounts: List with all the amounts to convert
        :param rate: conversion rate
        :param amount_decimal_places: decimal places of all the amounts
        :return: list containing the converted amounts
        """

        trace(INFO, "Converting - soft rounding")
        converted_amounts = []
        for amount in amounts:

            amount_value = int(amount) / Decimal(10 ** int(amount_decimal_places))
            converted_amount_value = amount_value * rate
            converted_amount_value = round(converted_amount_value, self.decimals) * 10

            if converted_amount_value - int(converted_amount_value) >= self.rounding_value:

                converted_amount_value = (int(converted_amount_value) + 1) * 10

            elif converted_amount_value - int(converted_amount_value) < self.rounding_value:

                converted_amount_value = (int(converted_amount_value) * 10)

            else:
                trace(DEBUG, "Math failed")

            str_converted_amount_value = str(converted_amount_value)

            if len(str_converted_amount_value) == 1:
                str_converted_amount_value = "{}{}".format("00", str_converted_amount_value)

            elif len(str_converted_amount_value) == 2:
                str_converted_amount_value = "{}{}".format("0", str_converted_amount_value)

            converted_amounts.append(str_converted_amount_value)

        return converted_amounts

    def launch_conversion(self, dict_request):
        """
        This function handles the currency conversion given a rest request
        :return: the json response
        """

        trace(INFO, "Entering currency conversion")

        self.response['toCurrency'] = dict_request['toCurrency']

        for dict_provider in dict_request['amounts']:

            provider_response = dict()
            provider_response['provider'] = dict_provider['provider']
            provider_response['fromCurrency'] = dict_provider['fromCurrency']

            # if same currency in/out
            if dict_request['toCurrency'] == dict_provider['fromCurrency']:
                provider_response['amounts'] = dict_provider['amounts']
                provider_response['amountDecimalPlaces'] = dict_provider['amountDecimalPlaces']
                self.response['convertedAmounts'].append(provider_response)
            else:
                # if rate is defined (after sales flow) we use the one in the request
                if 'rate' in dict_provider and 'rateDecimalPlaces' in dict_provider:
                    rate = [dict_provider['rate'], dict_provider['rateDecimalPlaces']]
                else:
                    rate = self.select_rule(dict_request['pos'], dict_request['distributor'],
                                            dict_request['toCurrency'], dict_provider)

                # if a rule is found
                if isinstance(rate, list):
                    rate_value = int(rate[0]) / Decimal(10 ** int(rate[1]))

                    provider_response['rate'] = str(rate[0])
                    provider_response['rateDecimalPlaces'] = str(rate[1])

                    trace(INFO, "Result rule check {}".format(rate))

                    converted_amounts = self.convert_hard_rounding(dict_provider['amounts'], rate_value,
                                                                   dict_provider['amountDecimalPlaces'])

                    provider_response['amounts'] = converted_amounts

                    provider_response['amountDecimalPlaces'] = "2"

                    self.response['convertedAmounts'].append(provider_response)
                else:
                    trace(INFO, "No rule found")

                    self.response['warnings'] = [CurrencyConverterHelper.warning_no_rate]

        return self.response
