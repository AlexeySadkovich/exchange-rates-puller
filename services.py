from datetime import timedelta, datetime
from typing import Dict

import xmltodict
from zeep import Client
from lxml import etree

SERVICE_URL = "http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL"
DELTA_TIME = timedelta(days=1)


def get_rates(date_from: str, date_to: str, currency: str) -> Dict:
    date_from = datetime.strptime(date_from, "%Y-%m-%d")
    date_to = datetime.strptime(date_to, "%Y-%m-%d")

    rates = _request_rates(date_from, date_to)

    if currency == "All":
        return rates

    result = {}

    for i in rates:
        index = 0
        for curr in rates[i]:
            if curr["VchCode"] == currency:
                result[i] = {}
                result[i][index] = curr
                index += 1

    return result


def _request_rates(date_from: datetime, date_to: datetime) -> Dict:
    """Return information about currency rates from cbr web service"""
    result = {}
    start_date = date_from

    while start_date <= date_to:
        client = Client(SERVICE_URL)
        xml = client.service.GetCursOnDateXML(start_date)

        # Parse response from cbr service
        xml_str = etree.tostring(xml)
        currency_data = xmltodict.parse(xml_str)['ValuteData']['ValuteCursOnDate']

        date = start_date.strftime("%Y-%m-%d")
        result[date] = currency_data

        start_date += DELTA_TIME

    return result
