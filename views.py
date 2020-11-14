import json

from flask import request, render_template

import services
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rates/get', methods=['POST'])
def get_rates():
    """Return exchange rates for the period specified by
     date-from and date-to fields in request"""
    data = request.get_json()

    result = services.get_rates(data["date-from"], data["date-to"], data["currency"])
    response = json.dumps(result)

    return response
