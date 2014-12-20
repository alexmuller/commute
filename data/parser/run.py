import datetime
import json
import os

import mollusc
import strava

def json_serialiser(obj):
    """Serialise datetime dates as part of a JSON file"""
    if isinstance(obj, datetime.date):
        return obj.isoformat()

STRAVA_ACCESS_TOKEN = os.environ['STRAVA_ACCESS_TOKEN']

strava_data = strava.fetch(STRAVA_ACCESS_TOKEN)

MOLLUSC_AUTH = (
    os.environ['MOLLUSC_BASIC_AUTH_USER'],
    os.environ['MOLLUSC_BASIC_AUTH_PASS'],
)

MOLLUSC_ENDPOINT = os.environ['MOLLUSC_ENDPOINT']

mollusc_data = mollusc.fetch(MOLLUSC_ENDPOINT, MOLLUSC_AUTH)

data = strava_data + mollusc_data

data.sort(key=lambda day: day['date'], reverse=True)

with open('../data.json', 'w') as outfile:
    json.dump(data, outfile, default=json_serialiser, indent=4)
