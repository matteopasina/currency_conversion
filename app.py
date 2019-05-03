#!/usr/bin/env python

from flask import Flask, request
from core.rates_retriever import RateRetriever
from data.constants import *

app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        return convert(request)


@app.route('/rate', methods=['GET'])
def rate():
    if request.method == 'GET':
        rr = RateRetriever(RATES_FILE)
        return rr.get_rates(request.args.get('currency'))


if __name__ == '__main__':
    app.run(debug=True)