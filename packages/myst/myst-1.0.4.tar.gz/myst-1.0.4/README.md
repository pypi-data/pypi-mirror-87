# Myst Python Library

This is the official Python client library for the Myst Platform.

### Requirements

- Python 2.7+ or Python 3.4+

### Installation

To install the package from PyPI:

    $ pip install --upgrade myst

### Authentication

The Myst API uses JSON Web Tokens (JWTs) to authenticate requests. The Myst Python library handles the sending of JWTs to the API automatically and
currently supports two ways to authenticate to obtain a JWT: through your Google user account or a Myst service account.

#### Authenticating using your user account

If you don't yet have a Google account, you can create one on the [Google Account Signup](https://accounts.google.com/signup) page.

Once you have access to a Google account, send an email to `support@myst.ai` with your email so we can authorize you to use the Myst Platform.

Use the following code snippet to authenticate using your user account:

```python
import myst

myst.authenticate()
```

The first time you run this, you'll be presented with a web browser and asked to authorize the Myst Python library to make requests on behalf of your Google user account.

#### Authenticating using a service account

You can also authenticate using a Myst service account. To request a service account, email `support@myst.ai`.

To authenticate using a service account, set the `MYST_APPLICATION_CREDENTIALS` environment variable to the path to your service account
key file and specify `use_service_account=True`:

```sh
$ export MYST_APPLICATION_CREDENTIALS=</path/to/key/file.json>
```

```python
import myst

myst.authenticate(use_service_account=True)
```

You can also explicitly pass the path to your service account key when authenticating:

```python
import myst

myst.authenticate(
    use_service_account=True,
    service_account_key_file_path='/path/to/key/file.json',
)
```

### Working with time series

The Myst python library currently supports listing, getting, and fetching data for time series.

#### Listing time series

```python
import myst

myst.authenticate()

all_time_series = myst.TimeSeries.list()
```

#### Getting a time series

```python
import myst

myst.authenticate()

time_series = myst.TimeSeries.get('fc84...')
```

#### Fetching data from a time series

You can either fetch data by specifying absolute start and end times, or offsets relative to the `as_of_time`. If no `as_of_time` is given,
it is assumed to mean "as of now":

```python
import datetime
import pytz

import myst

myst.authenticate(...)

time_series = myst.TimeSeries.get('fc84...')

# Fetching data using absolute start and end times.
data_series = time_series.fetch_data_series(
    start_time=datetime.datetime(2019, 1, 1),
    end_time=datetime.datetime(2019, 1, 2),
)

# Fetching data specifying an as of time.
data_series = time_series.fetch_data_series(
    start_time=datetime.datetime(2019, 1, 1),
    end_time=datetime.datetime(2019, 1, 2),
    as_of_time=datetime.datetime(2019, 1, 1, 12),
)

# Fetching data using offsets relative to now.
data_series = time_series.fetch_data_series(
    start_offset=datetime.timedelta(hours=-12),
    end_offset=datetime.timedelta(hours=12),
)

# Fetching data specifying a combination of relative offsets and absolute timestamps.
data_series = time_series.fetch_data_series(
    start_offset=datetime.timedelta(hours=-12),
    end_time=datetime.datetime(2019, 1, 2),
)
```

## Support

For questions or just to say hi, reach out to `support@myst.ai`.
