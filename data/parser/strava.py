import logging

from stravalib.client import Client

from helpers import timedelta_to_minutes

logging.basicConfig()

def filter_activities(activities):
    """Filter a list of Strava activities to return only those
       which are cycle commutes."""
    for activity in activities:
        if activity.type == 'Ride' and activity.commute:
            yield activity


def fetch(strava_access_token):
    """Fetch, filter and transform activities from Strava."""
    client = Client(access_token=strava_access_token)

    athlete = client.get_athlete()

    print "Fetching activities for {0} {1}".format(athlete.firstname, athlete.lastname)

    activities = client.get_activities()

    parsed_activities = []

    for activity in filter_activities(activities):
        parsed_activities.append({
            'mode': 'cycling',
            'duration': timedelta_to_minutes(activity.elapsed_time),
            'timestamp': activity.start_date_local,
        })

    return parsed_activities
