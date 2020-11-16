import sys
from datetime import timedelta, datetime
from typing import List

import xmltodict
from zeep import Client
from lxml import etree

SERVICE_URL = "http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL"
DELTA_TIME = timedelta(days=1)


def get_rates(date_from: str, date_to: str, currency: str) -> List:
    date_from = datetime.strptime(date_from, "%Y-%m-%d")
    date_to = datetime.strptime(date_to, "%Y-%m-%d")

    rates = _request_rates(date_from, date_to)
    result = []

    # Take only necessary information
    for i in rates:
        entry = {"date": i["date"], "data": []}

        for curr in i["data"]:
            if currency == "All" or currency == curr["VchCode"]:
                entry["data"].append(curr)

        result.append(entry)

    return result


def _request_rates(date_from: datetime, date_to: datetime) -> List:
    """Return information about currency rates from cbr web service.
        result: [{
            date:
            data: [
                {Vname: , Vnom: , Vcurs: , Vcode: , VchCode: ,},
                ...
            ]
        }, ...]
    """
    result = []
    current_date = date_from

    client = Client(SERVICE_URL)

    while current_date <= date_to:
        entry = {}
        xml = client.service.GetCursOnDateXML(current_date)

        # Parse response from cbr service
        xml_str = etree.tostring(xml)
        currency_data = xmltodict.parse(xml_str)['ValuteData']['ValuteCursOnDate']

        entry["date"] = current_date.strftime("%Y-%m-%d")
        entry["data"] = currency_data
        result.append(entry)

        current_date += DELTA_TIME

    return result
