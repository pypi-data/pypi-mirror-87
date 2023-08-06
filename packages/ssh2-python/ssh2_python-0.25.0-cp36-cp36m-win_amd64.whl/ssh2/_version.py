
import json

version_json = '''
{"date": "2020-12-06T17:25:18.912756", "dirty": false, "error": null, "full-revisionid": "ad1010fe5b7d4d82361b00e4017857bb7f36e46f", "version": "0.25.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

