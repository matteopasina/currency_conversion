import unittest
import json
from datetime import datetime
from core.rates_retriever import RateRetriever
from unittest.mock import Mock, patch
from data.constants import *


class TestRateRetriever(unittest.TestCase):
    def setUp(self):
        # Mocked timestamp in never older than 24h
        with open(MOCKED_RATES_FILE, 'r') as rates:
            mocked_rates_file = json.load(rates)
        if mocked_rates_file:
            mocked_rates_file['timestamp'] = datetime.now().timestamp()
            with open(MOCKED_RATES_FILE, 'w') as rates:
                json.dump(mocked_rates_file, rates, indent=4)

        self.retriever = RateRetriever(MOCKED_RATES_FILE)

    def test_get_rates(self):
        expected_response = {
            "CZK": 22.9508,
            "PLN": 3.8174,
            "EUR": 0.8923
        }
        response = self.retriever.get_rates(None)
        self.assertEqual(response, expected_response)

    def test_get_rates_with_currency(self):
        expected_response = dict()
        expected_response['EUR'] = 0.8923
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
        self.retriever._update_rates()
        with open(MOCKED_RATES_FILE, 'r') as rates:
            file_written = json.load(rates)
        self.assertDictEqual(file_written, self.retriever.conversion_rates)

'''
    @patch('core.requests.get')
    def test_call_api(self, mock_get):
        # Configure the mock to return a response with an OK status code.
        mock_get.return_value.ok = True

        # Call the service, which will send a request to the server.
        response = self.retriever._call_api()

        # If the request is sent successfully, then I expect a response to be returned.
        print(response)
'''


if __name__ == '__main__':
    unittest.main()
