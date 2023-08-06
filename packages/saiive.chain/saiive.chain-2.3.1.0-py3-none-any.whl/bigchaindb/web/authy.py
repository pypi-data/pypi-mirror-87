from flask_httpauth import HTTPBasicAuth

from bigchaindb import config
import os

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    
    config_bigchaindb = config['server']

    basic_enabled = config_bigchaindb['basic_enabled']

    if not basic_enabled:
        return True

    user = config_bigchaindb['basic_user']
    password = config_bigchaindb['basic_password']

    return username == user and  password == password