# -*- coding: utf-8 -*-
import os
_token = None
_DBCredentials = None

def getDBCredentials():
    global _DBCredentials
    if not _DBCredentials:
        _DBCredentials = os.environ['DB_CREDENTIALS']
    return _DBCredentials


def getTelegramToken():
    global _token
    if not _token:
        _token = os.environ['TELEGRAM_TOKEN']
    return _token

LATTER_A = 'a'
LATTER_B = 'b'

# Interval in hours
PARSE_INTERVAL = 1
