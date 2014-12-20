import requests

from bs4 import BeautifulSoup
from datetime import datetime
from random import normalvariate
from requests.auth import HTTPBasicAuth

from helpers import timedelta_to_minutes


def calculate_duration(start, end, duration):
    if start and end:
        return end - start
    elif duration:
        return int(round(normalvariate(duration, 2)))
    else:
        raise RuntimeError("Insufficient parameters to calculate duration")


def fetch(endpoint, auth):
    r = requests.get(endpoint,
                     auth=HTTPBasicAuth(auth[0], auth[1]))

    if r.status_code != 200:
        raise RuntimeError('Error connecting to Mollusc')

    mollusc_parsed = BeautifulSoup(r.text)

    debits = mollusc_parsed.find_all('tr', class_='debit')

    parsed_travels = []

    JOURNEY_DETAILS = {
        'Bus journey, route 9': {
            'related_segments': {
                'pre': {
                    'duration': 50,
                    'mode': 'walking',
                },
                'post': {
                    'duration': 10,
                    'mode': 'walking',
                },
            },
            'duration': 50,
            'mode': 'bus',
        },
        'Bus journey, route 94': {
            'duration': 30,
            'mode': 'bus',
        },
        'Holborn to Turnham Green': {
            'duration': None,
            'mode': 'tube',
        },
        'Tower Hill to Turnham Green': {
            'duration': None,
            'mode': 'tube',
        },
        'Turnham Green to Holborn': {
            'duration': None,
            'mode': 'tube',
        },
        'Turnham Green to Tower Hill': {
            'duration': None,
            'mode': 'tube',
        },
    }

    unsorted_journeys = []

    commute_date = datetime.now()

    for debit in debits:
        if 'newDate' in debit['class']:
            commute_date = datetime.strptime(debit['id'], '%Y-%m-%d').date()

        if commute_date.isoweekday() not in range(1, 6):
            # This is on a weekend so it's probably not a commute
            continue

        date_cell = debit.find('td', class_='date').get_text().strip()
        journey_start_time = datetime.strptime(date_cell[7:12], '%H:%M')
        journey_end_time = datetime.strptime(date_cell[-5:], '%H:%M')

        if journey_start_time.hour not in (range(6, 10) + range(16, 19)):
            # This happened outside of commuting hours
            continue

        this_days_commutes = [
            day for day in parsed_travels if day['date'] == commute_date]

        journey_description = debit.find(
            'td', class_='location').get_text().strip()

        if journey_description in JOURNEY_DETAILS:
            this_commute = JOURNEY_DETAILS[journey_description]

            segment = {
                'mode': this_commute['mode'],
            }

            if segment['mode'] == 'bus':
                segment['duration'] = calculate_duration(
                    None, None, this_commute['duration'])
            elif segment['mode'] == 'tube':
                duration = calculate_duration(
                    journey_start_time, journey_end_time, None)
                segment['duration'] = timedelta_to_minutes(duration)
            else:
                raise RuntimeError('Unknown segment mode')

            segments = []

            if 'related_segments' in this_commute:
                if 'pre' in this_commute['related_segments']:
                    segments.append(this_commute['related_segments']['pre'])

            segments.append(segment)

            if 'related_segments' in this_commute:
                if 'post' in this_commute['related_segments']:
                    segments.append(this_commute['related_segments']['post'])

            if this_days_commutes:
                this_days_commutes[0]['segments'] += segments
            else:
                parsed_travels.append({
                    'date': commute_date,
                    'segments': segments,
                })
        else:
            unsorted_journeys.append(journey_description)

    return parsed_travels
