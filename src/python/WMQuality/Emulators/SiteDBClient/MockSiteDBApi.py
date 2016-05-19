#! /usr/bin/env python

"""
Version of SiteDB.SiteDBJSON intended to be used with mock or unittest.mock
"""
from __future__ import (division, print_function)

import pdb


class MockSiteDBApi(object):
    def __init__(self):
        print("Initializing MockDBSApi")
