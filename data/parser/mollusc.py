import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from random import normalvariate
from requests.auth import HTTPBasicAuth

from helpers import timedelta_to_minutes

BUS_9_TO_GDS = 50
BUS_94_TO_GDS = 30
WALK_ALDWYCH_TO_GDS = 10
WALK_CHISWICK_TO_94_BUS = 10
WALK_CHISWICK_TO_HSMITH = 40
WALK_CHISWICK_TO_TURNHAM_GRN = 15
WALK_HOLBORN_TO_GDS = 5
WALK_OXFORD_CIRCUS_TO_GDS = 25
WALK_TOWER_HILL_TO_NI = 10

def calculate_duration(start, end, duration_delta):
    if start and end:
        delta = timedelta_to_minutes(end - start)
    elif duration_delta:
        minutes = timedelta_to_minutes(duration_delta)
        delta = int(round(normalvariate(minutes, 2)))
    else:
        raise RuntimeError("Insufficient parameters to calculate duration")

    return delta


def fetch(endpoint, auth):
    r = requests.get(endpoint,
                     auth=HTTPBasicAuth(auth[0], auth[1]))

    if r.status_code != 200:
        raise RuntimeError('Error connecting to Mollusc')

    mollusc_parsed = BeautifulSoup(r.text)

    debits = mollusc_parsed.find_all('tr', class_='debit')

    parsed_travels = []

    COMMUTE_METADATA = {
        'Bus journey, route 9': {
            'related_segments': [
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_CHISWICK_TO_HSMITH),
                    'offset': timedelta(minutes=-WALK_CHISWICK_TO_HSMITH),
                },
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_ALDWYCH_TO_GDS),
                    'offset': timedelta(minutes=1),
                }
            ],
            'duration': timedelta(minutes=BUS_9_TO_GDS),
            'mode': 'bus',
        },
        'Bus journey, route 94': {
            'related_segments': [
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_CHISWICK_TO_94_BUS),
                    'offset': timedelta(minutes=-WALK_CHISWICK_TO_94_BUS),
                },
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_OXFORD_CIRCUS_TO_GDS),
                    'offset': timedelta(minutes=1),
                }
            ],
            'duration': timedelta(minutes=BUS_94_TO_GDS),
            'mode': 'bus',
        },
        'Holborn to Turnham Green': {
            'related_segments': [
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_HOLBORN_TO_GDS),
                    'offset': timedelta(minutes=-WALK_HOLBORN_TO_GDS),
                },
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_CHISWICK_TO_TURNHAM_GRN),
                    'offset': timedelta(minutes=1),
                }
            ],
            'duration': None,
            'mode': 'tube',
        },
        'Tower Hill to Turnham Green': {
            'related_segments': [
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_TOWER_HILL_TO_NI),
                    'offset': timedelta(minutes=-WALK_TOWER_HILL_TO_NI),
                },
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_CHISWICK_TO_TURNHAM_GRN),
                    'offset': timedelta(minutes=1),
                }
            ],
            'duration': None,
            'mode': 'tube',
        },
        'Turnham Green to Holborn': {
            'related_segments': [
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_CHISWICK_TO_TURNHAM_GRN),
                    'offset': timedelta(minutes=-WALK_CHISWICK_TO_TURNHAM_GRN),
                },
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_HOLBORN_TO_GDS),
                    'offset': timedelta(minutes=1),
                }
            ],
            'duration': None,
            'mode': 'tube',
        },
        'Turnham Green to Tower Hill': {
            'related_segments': [
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_CHISWICK_TO_TURNHAM_GRN),
                    'offset': timedelta(minutes=-WALK_CHISWICK_TO_TURNHAM_GRN),
                },
                {
                    'mode': 'walking',
                    'duration': timedelta(minutes=WALK_TOWER_HILL_TO_NI),
                    'offset': timedelta(minutes=1),
                }
            ],
            'duration': None,
            'mode': 'tube',
        },
    }

    unsorted_journeys = []

    commute_datetime = datetime.now()

    for debit in debits:
        if 'newDate' in debit['class']:
            date_string = debit['id']

        date_cell = debit.find('td', class_='date').get_text().strip()
        time_start_string = date_cell[7:12]
        time_end_string = date_cell[-5:]

        datetime_format = '%Y-%m-%d %H:%M'

        commute_start = datetime.strptime(
            '{0} {1}'.format(date_string, time_start_string), datetime_format)
        commute_end = datetime.strptime(
            '{0} {1}'.format(date_string, time_end_string), datetime_format)

        if commute_start.isoweekday() not in range(1, 6):
            # This is on a weekend so it's probably not a commute
            continue

        if commute_start.hour not in (range(6, 10) + range(16, 19)):
            # This happened outside of commuting hours
            continue

        journey_description = debit.find(
            'td', class_='location').get_text().strip()

        if journey_description in COMMUTE_METADATA:
            metadata = COMMUTE_METADATA[journey_description]
            mode = metadata['mode']

            if mode == 'bus':
                duration = calculate_duration(None, None, metadata['duration'])
                commute_end = commute_start + metadata['duration']
            elif mode == 'tube':
                duration = calculate_duration(commute_start, commute_end, None)
            else:
                raise RuntimeError('Unknown segment mode')

            for segment in metadata['related_segments']:
                offset = segment['offset']

                if offset.total_seconds() < 0:
                    timestamp = commute_start + offset
                else:
                    timestamp = commute_end + offset

                this_segment = {
                    'mode': segment['mode'],
                    'duration': calculate_duration(None, None, segment['duration']),
                    'timestamp': timestamp,
                }

                parsed_travels.append(this_segment)

            main_segment = {
                'mode': metadata['mode'],
                'duration': duration,
                'timestamp': commute_start,
            }

            parsed_travels.append(main_segment)
        else:
            unsorted_journeys.append(journey_description)

    return parsed_travels
