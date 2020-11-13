import json
from datetime import datetime

import xmltodict
from flask import request, render_template
from zeep import Client
from app import app

from lxml import etree

SERVICE_URL = "http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get/rates', methods=['POST'])
def get_rates():
    """Return exchange rates for the period from date-from to date-to field"""
    data = request.get_json()
    print(data)

    client = Client(SERVICE_URL)
    xml = client.service.GetCursOnDateXML(data['date-from'])

    xml_str = etree.tostring(xml)
    currency_data = xmltodict.parse(xml_str)['ValuteData']['ValuteCursOnDate']

    response = json.dumps(currency_data)

    return response
