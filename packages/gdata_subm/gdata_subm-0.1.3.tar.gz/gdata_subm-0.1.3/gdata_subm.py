# 
# This is a library for building the JSON to submit to this server
# This handles key/values and submits them to the specified server
#

import json
import logging
import time
from socket import gethostname
from typing import List, Optional, Dict, Any
from urllib.request import (
    HTTPBasicAuthHandler,
    build_opener,
    HTTPPasswordMgrWithDefaultRealm,
)


class DataError(Exception):
    pass


class Gdata:
    """
    Key names are built in the following manner:

    plugin.\
        [plugin_instance].\
        [dtype (if diff. than plugin].\
        [dtype_instance].\
        [dsname (if not "value")]
    """

    def __init__(
            self,
            plugin: str,  # The name of your thing
            dstypes: List[str],  # The list of types: gauge, derive, counter
            values: List[float], # The corresponding list of values
            host: Optional[str]=None,
            plugin_instance: Optional[str]='',
            dtype: Optional[str]=None,
            dtype_instance: Optional[str]='',
            dsnames: Optional[List[str]]=None,
            interval: Optional[float]=10.0) -> None:
        self.plugin = plugin
        self.dstypes = dstypes
        self.values = [float(v) for v in values]
        self.plugin_instance = plugin_instance
        self.dtype = dtype
        self.dtype_instance = dtype_instance
        self.dsnames = dsnames
        self.interval = float(interval)
        self.host = host if host else self._get_hostname()
        self._validate_data()

    def to_dict(self) -> Dict[str, Any]:
        ret = {
            'values': self.values,
            'dstypes': self.dstypes,
            'dsnames': self.dsnames if self.dsnames else ['value'],
            'time': time.time(),
            'interval': self.interval,
            'host': self.host,
            'plugin': self.plugin,
            'plugin_instance': self.plugin_instance,
            'type': self.dtype if self.dtype else self.plugin,
            'type_instance': self.dtype_instance,
        }

        return ret

    def _get_hostname(self) -> str:
        name = gethostname()
        if '.' in name:
            name = name.split('.')[0]

        return name

    def _validate_data(self):
        if len(self.dstypes) != len(self.values):
            raise DataError(
                'You must have the same number of dstypes as values')

        if self.dsnames and len(self.dsnames) != len(self.dstypes):
            raise DataError(
                'You must have the same number of dstypes as dsnames')

        if self.interval < 0:
            raise DataError(
                'Invalid interval {}, must be > 0'.format(self.interval))


class GdataSubmit:

    def __init__(self, username: str, password: str, url: str):
        self.username = username
        self.password = password
        self.url = url

    def send_data(self, data: List[Gdata]) -> bool:
        ret = True
        handler = self._get_auth_handler()
        opener = build_opener(self._get_auth_handler())

        resp = None
        
        try:
            resp = opener.open(
                self.url,
                json.dumps([d.to_dict() for d in data]).encode('utf-8'),
                timeout=5,
            )
        except Exception:
            logging.exception('Failed to open url: {}'.format(self.url))
            ret = False

        if resp and resp.getcode() != 200:
            logging.error(
                'Sending data returned code: {}'.format(resp.getcode()))
            ret = False

        return ret

    def _get_auth_handler(self) -> HTTPBasicAuthHandler:
        pmgr = HTTPPasswordMgrWithDefaultRealm()
        pmgr.add_password(
            None,
            self.url,
            self.username,
            self.password,
        )
        handler = HTTPBasicAuthHandler(pmgr)

        return handler


