from datetime import timedelta, datetime
from typing import Dict

import xmltodict
from zeep import Client
from lxml import etree

SERVICE_URL = "http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL"
DELTA_TIME = timedelta(days=1)


def request_rates(data_from: str, data_to: str) -> Dict:
    """Return information about currency rates from cbr web service"""
    result = {}
    data_from = datetime.strptime(data_from, "%Y-%m-%d")
    data_to = datetime.strptime(data_to, "%Y-%m-%d")
    start_date = data_from

    while start_date <= data_to:
        client = Client(SERVICE_URL)
        xml = client.service.GetCursOnDateXML(start_date)

        # Parse response from cbr service
        xml_str = etree.tostring(xml)
        currency_data = xmltodict.parse(xml_str)['ValuteData']['ValuteCursOnDate']

        date = start_date.strftime("%Y-%m-%d")
        result[date] = currency_data

        start_date += DELTA_TIME

    return result
