# Django timescaledb

A database backend for Timescaledb.

Based on [gist](https://gist.github.com/dedsm/fc74f04eb70d78459ff0847ef16f2e7a) from WeRiot.


## Quick start

1. Install via pip

```bash
pip install django-timescaledb
```

2. Use as DATABASE engine in settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'timescale',
        ...
    },
}
```

3. Use TimescaleDateTimeField in your models. A [hypertable](https://docs.timescale.com/latest/using-timescaledb/hypertables#react-docs) will automatically be created.

```python
from timescale.fields import TimescaleDateTimeField

class SensorLog(models.Model):
   date = TimescaleDateTimeField(interval="1 day")
   value = models.IntegerField()

```

4. Use TimeBucket to query data
```python
from django.db.models import Avg
from timescale.expressions import TimeBucket
from whatever.models import StockPrice

time_bucket = TimeBucket(interval="2 days", expressions="date")
avg_prices = StockPrice.objects.filter(date=time_bucket).annotate(price=Avg("price"))

```


### Custom DB backend

Use a custom PostgreSQL db backend like PostGIS.

```python
# Configure via settings.py

TIMESCALE_DB_BACKEND_BASE = "django.contrib.gis.db.backends.postgis"
```
