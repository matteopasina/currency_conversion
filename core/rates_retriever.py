import json
from datetime import datetime, timedelta

import requests

from data.constants import *


class RateRetriever:
    """
    This class retrieves the exchange rates from https://openexchangerates.org/ and updates a file
    It reads the file and if the rates are older that 24h it updates it
    """

    def __init__(self, rates_file):
        """
        :param rates_file: the path to the file that stores the rates
        """
        self.rates_file = rates_file
        self.conversion_rates = {}
        self.now = datetime.now()
        self.delta = timedelta(hours=24)
        self.response = dict()

    def get_rates(self, currency):
        """
        This method returns the conversion rates of a currency with respect of USD
        If the currency is not supported it returns an error
        If is USD it returns all the rates of the other currencies
        :param currency: the currency desired
        :return: the conversion rate of that currency from USD
        """
        if currency and currency not in CURRENCIES_SUPPORTED:
            self.response['ERROR'] = "Currency not supported"
            return self.response

        self.load_rates()

        if currency in self.conversion_rates['rates']:
            self.response[currency] = self.conversion_rates['rates'][currency]
        else:
            self.response = self.conversion_rates['rates']

        return self.response

    def load_rates(self):
        """
        This method loads the rates from the file or calls the api and updates the file
        """
        try:
            if self.rates_file:
                with open(self.rates_file, 'r') as rates:
                    self.conversion_rates = json.load(rates)

                if 'timestamp' in self.conversion_rates and self.conversion_rates['timestamp'] != "TEST":
                    timestamp_rates = datetime.fromtimestamp(self.conversion_rates['timestamp'])

                    # if file of rates is older than 24h, call api and update it
                    if self.delta < self.now - timestamp_rates:
                        print("Rates older than 24h: updating rates")
                        params = {'app_id': APP_ID,
                                  'symbols': CURRENCIES,
                                  'prettyprint': False,
                                  'show_alternative': False}
                        self._call_api(API_URL_LATEST, params)
                        self._update_rates()
        except Exception as e:
            print(e)
            self.response['ERROR'] = "Error while loading rates"

    def _call_api(self, url, params):
        """
        This method does a get call to the url in input with the parameters in input
        :param url: the url of the api to call
        :param params: the parameters of the call
        :return self.conversion_rates updated with api response or error in self.response
        """
        try:
            response_api = requests.get(url, params=params)
            if response_api.ok:
                self.conversion_rates = json.loads(response_api.content)
            else:
                self.response['ERROR'] = "Unable to call exchange rates API"
        except Exception as e:
            print(e)
            self.response['ERROR'] = "Error while calling exchange rates API"

    def _update_rates(self):
        """
        Updates the rates in the file
        """
        try:
            if self.conversion_rates:
                with open(self.rates_file, 'w') as rates:
                    json.dump(self.conversion_rates, rates, indent=4)
        except Exception as e:
            print(e)
            self.response['ERROR'] = "Error while updating rates"

