import unittest
import json
from datetime import datetime
from core.rates_retriever import RateRetriever


class TestRateRetriever(unittest.TestCase):
    def setUp(self):
        # Mocked timestamp in never older than 24h
        with open('mocked_rates.json', 'r') as rates:
            mocked_rates_file = json.load(rates)
        mocked_rates_file['timestamp'] = datetime.now().timestamp()
        with open('mocked_rates.json', 'w') as rates:
            json.dump(mocked_rates_file, rates, indent=4)

        self.retriever = RateRetriever('mocked_rates.json')

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


if __name__ == '__main__':
    unittest.main()
