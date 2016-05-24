#! /usr/bin/env python

"""
Version of SiteDB.SiteDBJSON intended to be used with mock or unittest.mock
"""
from __future__ import (division, print_function)

import pdb
from WMCore.WMBase import getTestBase
import os
import json

# Read in the data just once so that we don't have to do it for every test (in __init__)

mockData = {}
globalFile = os.path.join(getTestBase(), '..', 'data', 'Mock', 'SiteDBMockData.json')

try:
    with open(globalFile, 'r') as mockFile:
        mockDataGlobal = json.load(mockFile)
except IOError:
    mockDataGlobal = {}


class MockSiteDBApi(object):

    def __init__(self):
        print("Initializing MockDBSApi")
    
    def __getattr__(self, item):
        """
        __getattr__ gets called in case lookup of the actual method fails. We use this to return data based on
        a lookup table

        :param item: The method name the user is trying to call
        :return: The generic lookup function
        """
        self.item = item
        return self.genericLookup

    def genericLookup(self, *args, **kwargs):
        """
        This function returns the mocked DBS data

        :param args: positional arguments it was called with
        :param kwargs: named arguments it was called with
        :return: the dictionary that DBS would have returned
        """
        if kwargs:
            signature = '%s:%s' % (self.item, sorted(kwargs.iteritems()))
        else:
            signature = self.item

        try:
            if mockData[signature] == 'Raises HTTPError':
                raise HTTPError
            else:
                return mockData[signature]
        except KeyError:
            raise KeyError("DBS mock API could not return data for method %s, args=%s, and kwargs=%s ." %
                           (self.item, args, kwargs))
