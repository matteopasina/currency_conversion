import requests
import json
from datetime import datetime, timedelta
from data.constants import *


class RateRetriever:

    def __init__(self, rates_file):
        self.rates_file = rates_file
        self.conversion_rates = {}
        self.now = datetime.now()
        self.delta = timedelta(hours=24)
        self.response = dict()

    def get_rates(self, currency):
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
        if self.rates_file:
            with open(self.rates_file, 'r') as rates:
                self.conversion_rates = json.load(rates)

            timestamp_rates = datetime.fromtimestamp(self.conversion_rates['timestamp'])

            # if file of rates is older than 24h, call api and update it
            if self.delta < self.now - timestamp_rates:
                print("Rates older than 24h: updating rates")
                self.call_api()
                self.update_rates()

    def call_api(self):
        params = {'app_id': APP_ID,
                  'symbols': CURRENCIES,
                  'prettyprint': False,
                  'show_alternative': False}

        self.conversion_rates = json.loads(requests.get(API_URL_LATEST, params=params).content)

    def update_rates(self):
        with open(self.rates_file, 'w') as rates:
            json.dump(self.conversion_rates, rates, indent=4)

