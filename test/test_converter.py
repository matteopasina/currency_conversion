import unittest
import json
from decimal import Decimal
from datetime import datetime
from core.rates_retriever import RateRetriever
from core.converter import CurrencyConverter
from data.constants import *


class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        # Mocked timestamp in never older than 24h
        with open(MOCKED_RATES_FILE, 'r') as rates:
            mocked_rates_file = json.load(rates)
        if mocked_rates_file:
            mocked_rates_file['timestamp'] = datetime.now().timestamp()
            with open(MOCKED_RATES_FILE, 'w') as rates:
                json.dump(mocked_rates_file, rates, indent=4)

        self.retriever = RateRetriever(MOCKED_RATES_FILE)

    def test_currency_not_supported(self):
        expected_response = {"ERROR": "Currency not supported"}
        converter = CurrencyConverter('LEV', 'PLN', '7,83', self.retriever)
        response = converter.convert()
        self.assertDictEqual(response, expected_response)

    def test_convert(self):
        expected_response = {
            "converted_value": "1.3021",
            "from_currency": "CZK",
            "to_currency": "PLN",
            "original_value": "7.83",
            "conversion_rate": "0.1663",
            "timestamp": "TIME"
        }
        converter = CurrencyConverter('CZK', 'PLN', '7,83', self.retriever)
        response = converter.convert()
        response["timestamp"] = "TIME"
        self.assertDictEqual(response, expected_response)

    def test_convert_from_USD(self):
        expected_response = {
            "converted_value": "60.4634",
            "from_currency": "USD",
            "to_currency": "PLN",
            "original_value": "15.8389",
            "conversion_rate": "3.8174",
            "timestamp": "TIME"
        }
        converter = CurrencyConverter('USD', 'PLN', '15,8389', self.retriever)
        response = converter.convert()
        response["timestamp"] = "TIME"
        self.assertDictEqual(response, expected_response)

    def test_convert_to_USD(self):
        expected_response = {
            "converted_value": "1120.7000",
            "from_currency": "EUR",
            "to_currency": "USD",
            "original_value": "1000",
            "conversion_rate": "1.1207",
            "timestamp": "TIME"
        }
        converter = CurrencyConverter('EUR', 'USD', '1000', self.retriever)
        response = converter.convert()
        response["timestamp"] = "TIME"
        self.assertDictEqual(response, expected_response)

    def test_build_response(self):
        expected_response = {
            "converted_value": "8000.0000",
            "from_currency": "EUR",
            "to_currency": "USD",
            "original_value": "1000",
            "conversion_rate": "1.2890",
            "timestamp": "TIME"
        }
        converter = CurrencyConverter('EUR', 'USD', '1000', self.retriever)
        converted_value = Decimal('8000')
        conversion_rate = Decimal('1.289')
        converter._build_response(converted_value, conversion_rate)
        response = converter.response
        response["timestamp"] = "TIME"
        self.assertDictEqual(response, expected_response)

    def test_compute_conversion_rate_to_USD(self):
        expected_conversion_rate = Decimal('1.1207')
        converter = CurrencyConverter('EUR', 'USD', None, None)
        base = 'USD'
        rates = {
            "CZK": 22.9508,
            "PLN": 3.8174,
            "EUR": 0.8923
        }
        conversion_rate = converter._compute_conversion_rate(base, rates)
        self.assertEqual(conversion_rate, expected_conversion_rate)

    def test_compute_conversion_rate_from_USD(self):
        expected_conversion_rate = Decimal('0.8923')
        converter = CurrencyConverter('USD', 'EUR', None, None)
        base = 'USD'
        rates = {
            "CZK": 22.9508,
            "PLN": 3.8174,
            "EUR": 0.8923
        }
        conversion_rate = converter._compute_conversion_rate(base, rates)
        self.assertEqual(conversion_rate, expected_conversion_rate)

    def test_compute_conversion_rate(self):
        expected_conversion_rate = Decimal('0.1663')
        converter = CurrencyConverter('CZK', 'PLN', None, None)
        base = 'USD'
        rates = {
            "CZK": 22.9508,
            "PLN": 3.8174,
            "EUR": 0.8923
        }
        conversion_rate = converter._compute_conversion_rate(base, rates)
        self.assertEqual(conversion_rate, expected_conversion_rate)


if __name__ == '__main__':
    unittest.main()