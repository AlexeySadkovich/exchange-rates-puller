import json
from datetime import datetime

import xmltodict
from suds.client import Client
from flask import request
from zeep import Client
from app import app

from lxml import etree

SERVICE_URL = "http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL"


@app.route('/')
def index():
    return "s"


@app.route('/get/rates', methods=['POST'])
def get_rates():
    data = request.get_json()
    print(data)

    client = Client(SERVICE_URL)
    xml = client.service.GetCursOnDateXML(datetime.now())

    xml_str = etree.tostring(xml)
    currency_data = xmltodict.parse(xml_str)['ValuteData']['ValuteCursOnDate']

    response = json.dumps(currency_data)

    return response
