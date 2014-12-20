# Data parser

Uses the output from my [Mollusc][mollusc] install and
[Strava][strava] (specifically [my profile][strava-me]) to
generate a JSON file of commute data.

[mollusc]: https://github.com/jwheare/mollusc
[strava]: http://www.strava.com/
[strava-me]: http://www.strava.com/athletes/alexmuller

## Running

```bash
export MOLLUSC_BASIC_AUTH_USER=your_username
export MOLLUSC_BASIC_AUTH_PASS=your_password
export MOLLUSC_ENDPOINT=http://mollusc.your.domain/
STRAVA_ACCESS_TOKEN=your_token python run.py
```
