#! /usr/bin/env python
"""
Unit testing base class that turns on emulators
"""

from __future__ import (division, print_function)

import unittest

import mock

from WMQuality.Emulators.DBSClient.MockDbsApi import MockDbsApi
from WMQuality.Emulators.PhEDExClient.MockPhEDExApi import MockPhEDExApi
from WMQuality.Emulators.SiteDBClient.MockSiteDBApi import MockSiteDBApi


class EmulatedUnitTestCase(unittest.TestCase):
    """
    Class that can be imported to switch to 'mock'ed versions of
    services.

    FIXME: For now only DBS is mocked
    """

    def __init__(self, methodName='runTest', mockDBS=True, mockPhEDEx=False, mockSiteDB=False):  # FIXME: Default to False for both?
        self.mockDBS = mockDBS
        self.mockPhEDEx = mockPhEDEx
        self.mockSiteDB = mockSiteDB
        super(EmulatedUnitTestCase, self).__init__(methodName)

    def setUp(self):
        """
        Start the various mocked versions and add cleanups in case of exceptions

        TODO: parameters to turn off emulators individually
        """

        if self.mockDBS:
            self.dbsPatcher = mock.patch('dbs.apis.dbsClient.DbsApi', new=MockDbsApi)
            self.inUseDbsApi = self.dbsPatcher.start()
            self.addCleanup(self.dbsPatcher.stop)

        if self.mockPhEDEx:
            self.phedexPatcher = mock.patch('WMCore.Services.PhEDEx.PhEDEx.PhEDEx', new=MockPhEDExApi)
            self.phedexPatcher2 = mock.patch('WMCore.WorkQueue.WorkQueue.PhEDEx', new=MockPhEDExApi)
            self.inUsePhEDExApi = self.phedexPatcher.start()
            self.phedexPatcher2.start()
            self.addCleanup(self.phedexPatcher.stop)
            self.addCleanup(self.phedexPatcher2.stop)

        if self.mockSiteDB:
            self.siteDBPatcher = mock.patch('WMCore.Services.SiteDB.SiteDB.SiteDBJSON', new=MockSiteDBApi)
            self.inUseSiteDBApi = self.siteDBPatcher.start()
            self.addCleanup(self.siteDBPatcher.stop)

        return
