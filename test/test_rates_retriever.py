import unittest
import json
from core.rates_retriever import RateRetriever


class TestRateRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = RateRetriever('mocked_rates.json')

    def test_get_rates(self):
        expected_response = {'CZK': 22.9456, 'PLN': 3.81765, 'EUR': 0.892779}
        response = json.loads(self.retriever.get_rates(None))
        self.assertEqual(response, expected_response)

    def test_get_rates_with_currency(self):
        expected_response = 0.892779
        response = json.loads(self.retriever.get_rates('EUR'))
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
