import unittest

from core.multi_converter import MultiCurrencyConverter
from core.rates_retriever import RateRetriever
from data.constants import *


class TestMultiCurrencyConverter(unittest.TestCase):
    def setUp(self):
        retriever = RateRetriever(MOCKED_RATES_FILE)
        self.converter = MultiCurrencyConverter(retriever)

    def test_multi_convert(self):
        post_request = {
            "to_currency": "EUR",
            "amounts": [
                {
                    "from_currency": "USD",
                    "amounts": ["1", "2"]
                },
                {
                    "from_currency": "PLN",
                    "amounts": ["37", "2,89", "9.3"]
                }
            ]
        }
        expected_response = {
            "to_currency": "EUR",
            "converted-amounts": [
                {
                    "from_currency": "USD",
                    "converted_amounts": [
                        "0.8919",
                        "1.7838"
                    ]
                },
                {
                    "from_currency": "PLN",
                    "converted_amounts": [
                        "8.6469",
                        "0.675393",
                        "2.17341"
                    ]
                }
            ]
        }

        response = self.converter.multi_convert(post_request)
        self.assertDictEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()