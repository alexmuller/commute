def timedelta_to_minutes(delta):
    """Takes a timedelta and outputs the delta to the nearest minute."""
    return int(round(delta.total_seconds() / 60))
