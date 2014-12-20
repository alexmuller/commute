import datetime
import json
import os
import strava

def json_serialiser(obj):
    """Serialise datetime dates as part of a JSON file"""
    if isinstance(obj, datetime.date):
        return obj.isoformat()

STRAVA_ACCESS_TOKEN = os.environ['STRAVA_ACCESS_TOKEN']

data = strava.fetch(STRAVA_ACCESS_TOKEN)

with open('../data.json', 'w') as outfile:
    json.dump(data, outfile, default=json_serialiser, indent=4)
