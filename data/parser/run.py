import datetime
import json
import os

import mollusc
import strava

from itertools import groupby

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

data.sort(key=lambda day: day['timestamp'], reverse=True)

grouped_data = []

for key, group in groupby(data, lambda elem: elem['timestamp'].date()):
    morning = []
    evening = []

    for segment in list(group):
        datum = {
            'mode': segment['mode'],
            'duration': segment['duration'],
        }
        if segment['timestamp'].hour < 12:
            morning.append(datum)
        else:
            evening.append(datum)

    day = {
        'date': key,
        'morning': list(reversed(morning)),
        'evening': list(reversed(evening)),
    }
    grouped_data.append(day)

with open('../data.json', 'w') as outfile:
    json.dump(grouped_data, outfile, default=json_serialiser, indent=4)
