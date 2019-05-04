#!/usr/bin/env python

from flask import Flask, request
from core.rates_retriever import RateRetriever
from core.converter import CurrencyConverter
from data.constants import *
import json

app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def convert_multi():
    if request.method == 'POST':
        '''
        try:
            currency_request = request.get_json()
            if Validator(SWAGGER).validate(currency_request):
                trace(DEBUG, "Validation has been successful")
                response = CurrencyConverter().launch_conversion(currency_request)
                return jsonify(response), 201
           else:
                return jsonify(CurrencyConverterHelper.error_invalid_message), 400
        except Exception as error:
            trace(ERROR, "CurrencyConverter has encountered an error {}".format(error))
            return jsonify(CurrencyConverterHelper.error_message), 500
        '''
        pass


@app.route('/rate', methods=['GET'])
def rate():
    if request.method == 'GET':
        retriever = RateRetriever(RATES_FILE)
        return json.dumps(retriever.get_rates(request.headers.get('currency')), indent=4)


@app.route('/convert', methods=['GET'])
def convert():
    if request.method == 'GET':
        from_currency = request.headers.get('from_currency')
        to_currency = request.headers.get('to_currency')
        value = request.headers.get('value')
        retriever = RateRetriever(RATES_FILE)
        converter = CurrencyConverter(from_currency, to_currency, value, retriever)
        return json.dumps(converter.convert(), indent=4)


if __name__ == '__main__':
    app.run(debug=True)