from .api import _postJSON
import json
import io
import pandas as pd
from pandas.io.json import json_normalize

class DataFrame:

    def __init__(self, table=None, **kwargs):
        if table is None:
            return None
        
        codes = {"table": table,
        "format": "CSV",
        "variables": []}

        for key, values in kwargs.items():
            codes['variables'].append({"code": key, "values": values})
            
        self._params = codes

    @property
    def pandas(self):
        r = _postJSON('data', self._params)
        return pd.read_csv(io.StringIO(r.content.decode('utf-8')), sep=";")

    @property
    def params(self):
        print(json.dumps(self._params, indent=4, ensure_ascii=False))





