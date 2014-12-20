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

    spacer_segment = {
        'mode': 'spacer',
        'duration': 10,
    }

    for activity in filter_activities(activities):
        commute_date = activity.start_date_local.date()
        duration_minutes = timedelta_to_minutes(activity.elapsed_time)

        this_days_activities = [
            day for day in parsed_activities if day['date'] == commute_date]

        segment = {
            'mode': 'cycling',
            'duration': duration_minutes,
        }

        if this_days_activities:
            this_days_activities[0]['segments'].append(spacer_segment)
            this_days_activities[0]['segments'].append(segment)
        else:
            parsed_activities.append({
                'date': commute_date,
                'segments': [
                    segment,
                ],
            })

    return parsed_activities
