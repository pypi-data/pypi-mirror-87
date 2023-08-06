# Copyright © 2020 Interplanetary Database Association e.V.,
# BigchainDB and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

"""Healthcheck endpoint"""

import flask
from flask_restful import Resource
import platform
import datetime

from bigchaindb.web.views.base import base_ws_uri
from bigchaindb import version
from bigchaindb.web.websocket_server import EVENTS_ENDPOINT



class HealthCheck(Resource):
    def get(self):
        return {'alive': True, 'timestamp': datetime.datetime.now().timestamp() * 1000}

