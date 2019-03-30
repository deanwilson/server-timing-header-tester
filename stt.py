from flask import Flask, Response, request
from random import randint


app = Flask(__name__)


@app.route('/')
def homepage():
    resp = Response("Server-Timing header test")
    resp.headers['Server'] = "Flask Server Timing header test"

    if 'timing' in request.args.keys():
        timing_params = []

        # args is a multidict that allowes duplicate key names
        for param in request.args.getlist('timing'):
            expanded = __expand_timing(param)

            timing_params.append(expanded)

        timings = ','.join(timing_params)

        resp.headers['Server-Timing'] = timings
    else:
        resp.headers['Server-Timing'] = __build_defaults()

    return resp


def __build_defaults():
    """Provide a default set of values if no parameters are passed"""
    defaults = [
        "MISSED",
        "database;dur=123",
        "cache;dur=10;desc=cache_check"
    ]

    return ', '.join(defaults)


def __expand_timing(timing):
    """Expand a given timing value to its canonical form"""
    deconstructed = {}

    elements = timing.split(';')
    timing_name = elements.pop(0)

    for pair in elements:
        name, value = pair.split('=')
        deconstructed[name] = value

    if "dur" in deconstructed:
        if ".." in deconstructed['dur']:
            start, finish = deconstructed['dur'].split('..')
            deconstructed['dur'] = randint(int(start), int(finish))

    # build the string. Name is always set, others might not be
    expanded_pairs = ';'.join({"{}={}".format(v, deconstructed[v]) for v in deconstructed})

    # if expanded_pairs is empty join will still add a ';' ## TODO
    if expanded_pairs:
        expanded = ';'.join([timing_name, expanded_pairs])
    else:
        expanded = timing_name

    return expanded
