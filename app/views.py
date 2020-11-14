import json

from flask import request, render_template

from app import app
from . import database, services


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rates/get', methods=['POST'])
def get_rates():
    """Return exchange rates for the period specified by
     date-from and date-to fields in request"""
    data = request.get_json()

    currency_rates = services.get_rates(data["date-from"], data["date-to"], data["currency"])
    response = json.dumps(currency_rates)

    return response


@app.route('/rates', methods=['GET'])
def get_saved_rates():
    """Return list of currency rates saved in database"""
    currency_rates = database.get_all()
    response = json.dumps(currency_rates)
    return response


@app.route('/rates/save', methods=['POST'])
def save_rates():
    """Save exchange rates to database"""
    data = request.get_json()

    currency_rates = services.get_rates(data["date-from"], data["date-to"], data["currency"])
    name = f'{data["date-from"]}|{data["date-to"]}|{data["currency"]}'
    saved_entry = database.save(name, currency_rates)

    if saved_entry:
        return {name: currency_rates}

