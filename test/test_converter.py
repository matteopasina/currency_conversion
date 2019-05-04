import unittest
import json
import re
from datetime import datetime
from core.rates_retriever import RateRetriever
from core.converter import CurrencyConverter


class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        # Mocked timestamp in never older than 24h
        with open('mocked_rates.json', 'r') as rates:
            mocked_rates_file = json.load(rates)
        mocked_rates_file['timestamp'] = datetime.now().timestamp()
        with open('mocked_rates.json', 'w') as rates:
            json.dump(mocked_rates_file, rates, indent=4)

        self.retriever = RateRetriever('mocked_rates.json')

    def test_convert(self):
        expected_response = {
            "converted_value": "1.3024",
            "from_currency": "CZK",
            "to_currency": "PLN",
            "original_value": "7.83",
            "conversion_rate": "0.1663",
            "timestamp": "TIME"
        }
        converter = CurrencyConverter('CZK', 'PLN', '7,83', self.retriever)
        response = converter.convert()
        response["timestamp"] = "TIME"
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()