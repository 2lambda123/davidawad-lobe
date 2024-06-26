#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
contains some convenience functions
"""
import os
import json
import logging

from uszipcode import ZipcodeSearchEngine
import requests

DEBUG = os.environ.get('DEBUG', False)


logger = logging.getLogger('gunicorn.error')

CHASE_ENDPOINT = os.environ.get('CHASE_ENDPOINT')

#  application.logger.debug('this will show in the log')


def log(msg: str) -> None:
    """
    simple wrapper for logging to stdout on heroku
    """
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        formatted_msg = "{}".format(str(msg))
        print(formatted_msg)
        # logger doesn't work
        logger.debug(formatted_msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    # sys.stdout.flush()


def find_state_from_coords(lat, long) -> str:
    """
    determines the US state based on a particular set of coordinates
    """
    with ZipcodeSearchEngine() as search:

        res = search.by_coordinate(lat, long, radius=30)

        if not res:
            return None

        # get zipcode based on lat / long
        zipcode = res[0]['Zipcode']

        print(zipcode)

        if not zipcode:
            return None

        # use zipcode object to determine state
        zipcode_object = search.by_zipcode(zipcode)

        state = zipcode_object['State']  # NY

        return state


def chase_lookup(**kwargs):
    print(kwargs)
    r = requests.get(CHASE_ENDPOINT, json=kwargs, timeout=60)
    print (r.status_code)
    print (r.text)
    if r.status_code == 200:
        return r.json()
