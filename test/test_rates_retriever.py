import unittest
import json
from core.rates_retriever import RateRetriever


class TestRateRetriever(unittest.TestCase):
    def setUp(self):
        # TODO timestamp to be never more than 24h
        self.retriever = RateRetriever('mocked_rates.json')

    def test_get_rates(self):
        expected_response = {
            "CZK": 22.9508,
            "PLN": 3.8174,
            "EUR": 0.8923
        }
        response = json.loads(self.retriever.get_rates(None))
        self.assertEqual(response, expected_response)

    def test_get_rates_with_currency(self):
        expected_response = dict()
        expected_response['EUR'] = 0.8923
        response = self.retriever.get_rates('EUR')
        self.assertDictEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
