#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402


host = "localhost"
port = 4444
password = "secret"

ws = obsws(host, port, password)
ws.connect()

try:
    item = ws.call(requests.GetSceneItemProperties('Fond', 'Test'))
    print(item.getPosition())
    
    r = ws.call(requests.SetSceneItemProperties('Fond', 'Test', position={'x':50, 'y':50}))
    print(r)

    print("End of list")

except KeyboardInterrupt:
    pass

ws.disconnect()
