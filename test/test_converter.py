import unittest
from decimal import Decimal

from core.converter import CurrencyConverter
from core.rates_retriever import RateRetriever
from data.constants import *


class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.retriever = RateRetriever(MOCKED_RATES_FILE)

    def test_currency_not_supported(self):
        expected_response = {"ERROR": "Currency not supported"}
        converter = CurrencyConverter('LEV', 'PLN', '7,83', self.retriever)
        response = converter.convert()
        self.assertDictEqual(response, expected_response)

    def test_convert(self):
        expected_response = Decimal('1.302129')
        converter = CurrencyConverter('CZK', 'PLN', '7,83', self.retriever)
        response = converter.convert()
        self.assertEqual(response, expected_response)

    def test_convert_from_USD(self):
        expected_response = Decimal('60.46341686')
        converter = CurrencyConverter('USD', 'PLN', '15,8389', self.retriever)
        response = converter.convert()
        self.assertEqual(response, expected_response)

    def test_convert_to_USD(self):
        expected_response = Decimal('1121.2000')
        converter = CurrencyConverter('EUR', 'USD', '1000', self.retriever)
        response = converter.convert()
        self.assertEqual(response, expected_response)

    def test_build_response(self):
        expected_response = {
            "converted_value": "8000.0000",
            "from_currency": "EUR",
            "to_currency": "USD",
            "original_value": "1000",
            "conversion_rate": "1.2890",
            "timestamp": "TEST"
        }
        converter = CurrencyConverter('EUR', 'USD', '1000', self.retriever)
        converted_value = Decimal('8000')
        converter.conversion_rate = Decimal('1.289')
        response = converter.build_response(converted_value)
        response["timestamp"] = "TEST"
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