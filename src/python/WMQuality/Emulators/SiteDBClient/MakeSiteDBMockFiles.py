#!/usr/bin/env python
"""
MakeSiteDBMockFiles

Program to create mock SiteDB JSON files used by the SiteDB mock-based emulator
"""

from __future__ import (division, print_function)
from WMCore.Services.Service import Service
from WMCore.WMBase import getTestBase
import json
import os

def row2dict(columns, row):
    """Convert rows to dictionaries with column keys from description"""
    robj = {}
    for k,v in zip(columns, row):
        robj.setdefault(k,v)
    return robj

def unflattenJSON(data):
    """Tranform input to unflatten JSON format"""
    columns = data['desc']['columns']
    return [row2dict(columns, row) for row in data['result']]


class MakeSiteDBMockFiles(Service):
    
    def __init__(self, config={}):
        config = dict(config)
        config['endpoint'] = "https://cmsweb.cern.ch/sitedb/data/prod/"
        Service.__init__(self, config)

    def getJSON(self, callname, filename = 'result.json', clearCache = False, verb = 'GET', data={}):
        """
        _getJSON_

        retrieve JSON formatted information given the service name and the
        argument dictionaries

        TODO: Probably want to move this up into Service
        """
        result = ''
        if clearCache:
            self.clearCache(cachefile=filename, inputdata=data, verb = verb)
        try:
            #Set content_type and accept_type to application/json to get json returned from siteDB.
            #Default is text/html which will return xml instead
            #Add accept-encoding to gzip,identity to overwrite httplib default gzip,deflate,
            #which is not working properly with cmsweb
            f = self.refreshCache(cachefile=filename, url=callname, inputdata=data,
                                  verb = verb, contentType='application/json',
                                  incoming_headers={'Accept' : 'application/json',
                                                    'accept-encoding' : 'gzip,identity'})
            result = f.read()
            f.close()
        except IOError:
            raise RuntimeError("URL not available: %s" % callname )
        try:
            results = json.loads(result)
            results = unflattenJSON(results)
            return results
        except SyntaxError:
            self.clearCache(filename, inputdata=data, verb=verb)
            raise SyntaxError("Problem parsing data. Cachefile cleared. Retrying may work")

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
    x = MakeSiteDBMockFiles()
    func = getattr(x, 'getJSON')
    for call in calls:
        signature = str(sorted(call.iteritems()))
        try:
            result = func(**call) 
        except HTTPError:
            result = 'Raises HTTPError'
        lookup.update({signature:result})
    
    with open(outFilename, 'w') as mockData:
        json.dump(lookup, mockData, indent=1, separators=(',', ': '))
