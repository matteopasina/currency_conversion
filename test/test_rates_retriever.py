import unittest
import json
from datetime import datetime, timedelta
from unittest.mock import patch
from core.rates_retriever import RateRetriever
from data.constants import *


# Function to mock the get request
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code, ok):
            self.content = content
            self.status_code = status_code
            self.ok = ok

    if args[0] == 'https://openexchangerates.org/api/latest.json':
        mocked_content = {
            "disclaimer": "NO TERMS",
            "license": "MOCKEDLICENSE",
            "timestamp": 34239429042,
            "base": "USD",
            "rates": {
                "CZK": 2000,
                "EUR": 432,
                "PLN": 4344
            }
        }
        return MockResponse(json.dumps(mocked_content), 200, True)

    return MockResponse(None, 404, False)


class TestRateRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = RateRetriever(MOCKED_RATES_FILE)

    def test_get_rates(self):
        expected_response = {
            "CZK": 22.9508,
            "EUR": 0.89194,
            "PLN": 3.8174
        }
        response = self.retriever.get_rates(None)
        self.assertEqual(response, expected_response)

    def test_get_rates_with_currency(self):
        expected_response = dict()
        expected_response['EUR'] = 0.89194
        response = self.retriever.get_rates('EUR')
        self.assertDictEqual(response, expected_response)

    def test_currency_not_supported(self):
        expected_response = dict()
        expected_response['ERROR'] = "Currency not supported"
        response = self.retriever.get_rates('KIWI')
        self.assertDictEqual(response, expected_response)

    def test_load_rates_no_file(self):
        self.retriever = RateRetriever(None)
        self.assertDictEqual(self.retriever.conversion_rates, {})

    def test_load_rates(self):
        self.retriever = RateRetriever(MOCKED_RATES_FILE)
        self.retriever.conversion_rates = {
            "disclaimer": "Usage subject to terms: https://openexchangerates.org/terms",
            "license": "https://openexchangerates.org/license",
            "timestamp": 1557068423,
            "base": "USD",
            "rates": {
                "CZK": 22.9508,
                "EUR": 0.89194,
                "PLN": 3.8174
            }
        }
        self.retriever._update_rates()
        with open(MOCKED_RATES_FILE, 'r') as rates:
            file_written = json.load(rates)
        self.assertDictEqual(file_written, self.retriever.conversion_rates)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_call_api(self, mock_get):
        expected_get_response = {
            "disclaimer": "NO TERMS",
            "license": "MOCKEDLICENSE",
            "timestamp": 34239429042,
            "base": "USD",
            "rates": {
                "CZK": 2000,
                "EUR": 432,
                "PLN": 4344
            }
        }
        params = {'app_id': APP_ID,
                  'symbols': CURRENCIES,
                  'prettyprint': False,
                  'show_alternative': False}
        url = 'https://openexchangerates.org/api/latest.json'
        self.retriever.conversion_rates = {}

        self.retriever._call_api(url, params)

        self.assertEqual(expected_get_response, self.retriever.conversion_rates)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_timestamp(self, mock_get):
        self.retriever.rates_file = MOCKED_TIMESTAMP
        with open(self.retriever.rates_file, 'w') as rates:
            timestamp_5h_old = {"timestamp": (datetime.now() - timedelta(hours=5)).timestamp()}
            json.dump(timestamp_5h_old, rates, indent=4)

        self.retriever.load_rates()

        self.assertEqual(timestamp_5h_old, self.retriever.conversion_rates)

        with open(self.retriever.rates_file, 'w') as rates:
            timestamp_27h_old = {"timestamp": (datetime.now() - timedelta(hours=27)).timestamp()}
            json.dump(timestamp_27h_old, rates, indent=4)

        self.retriever.load_rates()

        self.assertEqual(34239429042, self.retriever.conversion_rates["timestamp"])

        self.retriever.rates_file = MOCKED_RATES_FILE

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_api_down(self, mock_get):
        expected_get_response = "Unable to call exchange rates API"
        params = {'app_id': APP_ID,
                  'symbols': CURRENCIES,
                  'prettyprint': False,
                  'show_alternative': False}
        url = 'wrong url'
        self.retriever.conversion_rates = {}

        self.retriever._call_api(url, params)

        self.assertEqual(expected_get_response, self.retriever.response['ERROR'])


if __name__ == '__main__':
    unittest.main()
