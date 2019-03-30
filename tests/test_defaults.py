import pytest

import stt


@pytest.fixture
def client():
    """Create the flask test client"""
    stt.app.config['TESTING'] = True
    flask_client = stt.app.test_client()
    yield flask_client


def extract_timings(timing):
    """Take a timing entry and return it as a dict"""
    expanded = {}
    elements = timing.split(';')

    expanded['name'] = elements.pop(0)

    for pair in elements:
        name, value = pair.split('=')
        expanded[name] = value

    return expanded

### Test the defaults


def test_default_index(client):
    """Test the default index returns a known string"""
    ret = client.get('/')
    assert b'Server-Timing header' in ret.data


def test_default_headers(client):
    """Test the default headers are correct"""
    ret = client.get('/')
    timings = ret.headers['Server-Timing'].split(',')

    assert "MISSED" in timings[0]

    cache = extract_timings(timings[-1])
    assert cache['desc'] == "cache_check"


### Test URL specified headers


def test_single_url_param(client):
    """Test that supplying values as URL params works"""

    ret = client.get('/?timing=mysql;dur=200;desc="database query"')
    timings = ret.headers['server-timing'].split(',')

    assert "mysql" in timings[0]


def test_multiple_url_params(client):
    """Test multiple timing URL parameters work"""

    params = "&".join([
        'timing=redis;dur=10;desc=cache',
        'timing=mysql;dur=200;desc="database query"',
        'timing=HIT',
    ])

    url = "/?{}".format(params)

    ret = client.get(url)
    timings = ret.headers['server-timing'].split(',')

    assert "mysql" in timings[1]
    assert timings[2] == "HIT"


def test_random_number_url_param(client):
    """Test range specifing parameters are expanded."""

    url = "/?timing=memcached;dur=200..300"

    ret = client.get(url)
    timings = ret.headers['server-timing'].split(',')
    timing = extract_timings(timings[0])

    assert timing['name'] == "memcached"
    assert int(timing['dur']) > 200
