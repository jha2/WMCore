#! /usr/bin/env python
"""
Unit testing base class that turns on emulators
"""

from __future__ import (division, print_function)

import unittest

import mock
from WMQuality.Emulators.DBSClient.MockDbsApi import MockDbsApi


class EmulatedUnitTest(unittest.TestCase):
    """
    Class that can be imported to switch to 'mock'ed versions of
    services.

    FIXME: For now only DBS is mocked
    """


    def setUp(self):
        # In python 2.7 code like this will be possible (making cleanup a sure thing
        # dbsPatcher = mock.patch('dbs.apis.dbsClient.DbsApi')
        # self.MockDbsApi = dbsPatcher.start()
        # self.addCleanup(dbsPatcher.stop)

        # For python 2.6 we need to cache this in self (may want to for inherited unit tests anyhow
        self.url = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader'
        self.dbs = MockDbsApi(self.url)
        self.dbsPatcher = mock.patch('dbs.apis.dbsClient.DbsApi', new=MockDbsApi)
        self.inUseDbsApi = self.dbsPatcher.start()
        return

    def tearDown(self):
        # Needed in python 2.6, not needed in 2.7 with addCleanup
        self.inUseDbsApi = self.dbsPatcher.stop()
        return

    def testListDatatiers(self):
        """
        listDatatiers returns all datatiers available
        self.dbs = DBSReader(self.endpoint)
        results = self.dbs.listDatatiers()
        self.assertTrue('RAW' in results)
        self.assertTrue('GEN-SIM-RECO' in results)
        self.assertTrue('GEN-SIM' in results)
        self.assertFalse('RAW-ALAN' in results)
        """
	#Get from DBS
        results =  self.dbs.listDataTiers()

	#Create mock instance
        instance = self.inUseDbsApi
        instance.listDataTiers = 'RAW'

	#Assert
        self.assertTrue(instance.listDataTiers in [result['data_tier_name'] for result in results])
        return


if __name__ == '__main__':
    unittest.main()
