import json

from bson import json_util
from flask import request, render_template

from app import app
import database, services


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/saved')
def saved():
    return render_template('saved.html')


@app.route('/rates/get', methods=['POST'])
def get_rates():
    """Return exchange rates for the period specified by
     date-from and date-to fields in request"""
    data = request.get_json()

    currency_rates = services.get_rates(data["date-from"], data["date-to"], data["currency"])
    response = json_util.dumps(currency_rates)

    return response


@app.route('/rates', methods=['GET'])
def get_saved_rates():
    """Return list of currency rates saved in database"""
    params = request.args

    currency_rates = database.get_rates_data(params)

    if len(currency_rates) > 0:
        response = json_util.dumps(currency_rates)
        return response, 200
    else:
        return {"detail": "Entries not found"}, 400


@app.route('/rates/save', methods=['POST'])
def save_rates():
    """Save exchange rates to database"""
    data = request.get_json()

    date_from = data["date-from"]
    date_to = data["date-to"]
    currency = data["currency"]

    currency_rates = services.get_rates(date_from, date_to, currency)

    entry = {
        "date-from": date_from,
        "date-to": date_to,
        "currency": currency,
        "entries": currency_rates
    }
    saved_entry = database.save(entry)

    if saved_entry:
        return json_util.dumps(entry)

