# Data parser

Uses a database dump from my [Mollusc][mollusc] install and
[Strava][strava] (specifically [my profile][strava-me]) to
generate a JSON file of commute data.

[mollusc]: https://github.com/jwheare/mollusc
[strava]: http://www.strava.com/
[strava-me]: http://www.strava.com/athletes/alexmuller

## Running

```bash
STRAVA_ACCESS_TOKEN=your_token python run.py
```
