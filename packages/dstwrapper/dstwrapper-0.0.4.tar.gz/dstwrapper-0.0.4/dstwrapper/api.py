import requests
import pandas as pd
import json
from requests.exceptions import HTTPError
from pandas.io.json import json_normalize

endpoints = {
    "tables": "https://api.statbank.dk/v1/tables",
    "tableinfo": "https://api.statbank.dk/v1/tableinfo",
    "data": "https://api.statbank.dk/v1/data"
}

def explore(key=None):
    if isinstance(key, str):
        params = {"table": key}
        r = _postJSON('tableinfo', params)
        _printInfo(json.loads(r.content))

    if isinstance(key, int) or key is None:
        try:
            r = requests.get(endpoints['tables'])
            r.raise_for_status()
            df = pd.DataFrame(json_normalize(r.json()))
            return df.head(key)

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None


def _postJSON(endpoint, params):
    try:
        r = requests.post(endpoints[endpoint], json=params)
        r.raise_for_status()
        return r

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None


def _printInfo(data):
    try:
        for var in data['variables']:
            print(var['id'])
            for v in var['values']:
                print(v)
            print('\n-------\n')
    except Exception as e:
        print(e)