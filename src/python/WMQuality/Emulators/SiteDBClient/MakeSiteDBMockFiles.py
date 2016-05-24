#!/usr/bin/env python
"""
MakeSiteDBMockFiles

Program to create mock SiteDB JSON files used by the SiteDB mock-based emulator
"""

from __future__ import (division, print_function)
from WMCore.Services.SiteDB.SiteDB import SiteDBJSON
from WMCore.WMBase import getTestBase
import json
import os

if __name__ =='__main__':
    calls = [
           # {'callname': 'people', 'filename': 'people.json', 'clearCache': False, 'verb': 'GET', 'data':{}},
            {'callname': 'site-names', 'filename': 'site-names.json', 'clearCache': False, 'verb': 'GET', 'data':{}},
            {'callname': 'site-resources', 'filename': 'site-resources.json', 'clearCache': False, 'verb': 'GET', 'data':{}},
            {'callname': 'data-processing', 'filename': 'data-processing.json', 'clearCache': False, 'verb': 'GET', 'data':{}}
            ]
    lookup = {}

    outFile = 'SiteDBMockData.json'
    outFilename = os.path.join(getTestBase(), '..', 'data', 'Mock', outFile)
    print(outFilename)
    x = SiteDBJSON()
    for call in calls:
        signature = str(sorted(call.iteritems()))
        try:
            result = x.getJSON(**call) 
        except HTTPError:
            result = 'Raises HTTPError'
        lookup.update({signature:result})
    
    with open(outFilename, 'w') as mockData:
        json.dump(lookup, mockData, indent=1, separators=(',', ': '))
