#!/usr/bin/env python

"""
Test case for SiteDB Emulator
"""

from __future__ import print_function

import unittest

from  WMQuality.Emulators.SiteDBClient.SiteDB import SiteDBJSON


class SiteDBEmulatorTest(unittest.TestCase):
    """
    Unit tests for SiteScreening module
    """

    def setUp(self):
        """
        Setup for unit tests
        """
        self.mySiteDB = SiteDBJSON()
        self.maxDiff = 2048

    def testCheckAndConvertSENameToPNN(self):
        """
        Test the conversion of SE name to PNN for single and multiple sites/PNNs using checkAndConvertSENameToPNN
        """

        fnalSE = u'cmssrm.fnal.gov'
        nebraskaSE = u'red-srm1.unl.edu'
        fnalPNNs = [u'T1_US_FNAL_Buffer', u'T1_US_FNAL_MSS']
        nebraskaPNN = [u'T2_US_Nebraska']

        pnnList = fnalPNNs + nebraskaPNN
        seList = [fnalSE, nebraskaSE]

        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN(fnalSE), fnalPNNs)
        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN([fnalSE]), fnalPNNs)

        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN(nebraskaSE), nebraskaPNN)
        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN([nebraskaSE]), nebraskaPNN)

        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN(seList), nebraskaPNN + fnalPNNs)

        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN(pnnList), pnnList)

        return


if __name__ == '__main__':
    unittest.main()
