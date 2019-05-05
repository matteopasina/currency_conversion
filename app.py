#!/usr/bin/env python

from flask import Flask, request
from core.rates_retriever import RateRetriever
from core.converter import CurrencyConverter
from core.multi_converter import MultiCurrencyConverter
from data.constants import *
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import yaml

app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def convert_multi():
    if request.method == 'POST':
        with open(SWAGGER, 'r') as swagger:
            try:
                schema = yaml.safe_load(swagger)
            except yaml.YAMLError as exc:
                print(exc)
        try:
            validate(request.get_json(), schema)
        except ValidationError as err:
            response = dict()
            response['ERROR'] = str(err)
            return json.dumps(response, indent=4)
        retriever = RateRetriever(RATES_FILE)
        converter = MultiCurrencyConverter(retriever)
        return json.dumps(converter.multi_convert(request.get_json()), indent=4)


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
        converted_value = converter.convert()
        return json.dumps(converter.build_response(converted_value), indent=4)


if __name__ == '__main__':
    app.run(debug=True)