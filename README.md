# server-timing-header-tester
A small webapp for generating Server-Timing headers

[![Actions Status](https://github.com/deanwilson/server-timing-header-tester/workflows/Python%20package/badge.svg)](https://github.com/deanwilson/server-timing-header-tester/actions)

## Introduction

The Server-Timing specification is a way to add semi-structured values
describing aspects of the response generation and how long each section
took to a HTTP request. These can then be processed and displayed in
your normal web development tools. This small flask application provides
a simple way to specify values for the `Server-Timing` header. It was written to
help provide a canned data source for some of my other projects.

You can learn more about the general usage of the header in my
[Show server side response timings in chrome developer tools](https://www.unixdaemon.net/tools/show-server-side-response-timings-in-chrome-developer-tools/) post.

## Usage

### Installation

I run all my python projects under `venvs` so the instructions below reflect
this:

    git clone https://github.com/deanwilson/server-timing-header-tester.git
    cd server-timing-header-tester

    # create the venv and activate it
    python3 -mvenv venv
    source venv/bin/activate

    # install the dependencies
    pip3 install -r requirements.txt

### Running the application

Now we've done all the preparation work we can run the application.

    FLASK_APP=stt flask run

    curl -I http://127.0.0.1:5000/
    Server-Timing: MISSED, database;dur=123, cache;dur=10;desc=cache_check

By default `stt` (Server-Timing Tester) returns a header with one of each type
of value. A base name, `MISSED`, a value with a duration, `database` and one
with both a duration and a description, `cache`.

To specify your own values you need to pass parameters named `timing` to
the application.

    # A single value
    curl -I 127.0.0.1:5000?timing='mysql;dur=200;desc=databasequery'
    # multiple values
    curl -I 127.0.0.1:5000?timing='mysql;dur=200;desc=databasequery&timing=crm;dur=400'

These values from these parameters will be reflected in the Server-Timing
header. One additional use case is the ability to specify a range in the
duration:

    curl -I 127.0.0.1:5000?timing='mysql;dur=200..400;desc=databasequery'

    ...
    Server: Flask Server Timing header test
    Server-Timing: mysql;desc=databasequery;dur=319
    ...

Specifying a lower and upper boundary in this format, `dur=200..400`, will cause
the application to replace it with a random value from inside the range. This
allows a small amount of dynamic behaviour when running the same request
repeatedly (and makes the graphs more interesting).

It's worth noting that you can pass the parameters to the application via a
web browser too. This allows you to view them in your normal web developer
tools.


## Testing

This application provides basic tests to ensure its behaviour is correct. They
are located in [/tests/](/tests/) and run under pytest.

    python3 -m pytest -v tests/

    tests/test_defaults.py::test_default_index PASSED                                     [ 20%]
    tests/test_defaults.py::test_default_headers PASSED                                   [ 40%]
    tests/test_defaults.py::test_single_url_param PASSED                                  [ 60%]
    tests/test_defaults.py::test_multiple_url_params PASSED                               [ 80%]
    tests/test_defaults.py::test_random_number_url_param PASSED                           [100%]


### Author

  [Dean Wilson](https://www.unixdaemon.net)
