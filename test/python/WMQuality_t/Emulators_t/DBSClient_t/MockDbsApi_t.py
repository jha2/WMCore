#!/usr/bin/env python

import unittest2
import mock
from nose.plugins.attrib import attr
from WMQuality.Emulators.DBSClient.MockDbsApi import MockDbsApi
from dbs.apis.dbsClient import DbsApi


class MockDbsApiTest(unittest2.TestCase):
    """
    Class that can be imported to switch to 'mock'ed versions of
    services.

    """

    def setUp(self):
        self.endpoint = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader'
        self.realDBS = DbsApi(self.endpoint)
        self.mockDBS = MockDbsApi(self.endpoint)
        self.dbsPatcher = mock.patch('dbs.apis.dbsClient.DbsApi', new=MockDbsApi)
        self.inUseDbsApi = self.dbsPatcher.start()
        return

    def tearDown(self):
        # Needed in python 2.6, not needed in 2.7 with addCleanup
        self.inUseDbsApi = self.dbsPatcher.stop()
        return

    def testListDataTiers(self):
	
        #Get from real and mock DBS
        result =  self.realDBS.listDataTiers()
        result_mock = self.mockDBS.listDataTiers()

        #assert the result
        self.assertItemsEqual(result, result_mock)

        return


if __name__ == '__main__':
    unittest2.main()

