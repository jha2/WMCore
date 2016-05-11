#!/usr/bin/env python
"""
Test case for SiteDB
"""
from __future__ import print_function

import pdb
import unittest

from WMCore.Services.SiteDB.SiteDB import SiteDBJSON
from WMCore.Services.EmulatorSwitch import EmulatorHelper
from WMQuality.Emulators.EmulatedUnitTestCase import EmulatedUnitTestCase

class SiteDBTest(EmulatedUnitTestCase):
    """
    Unit tests for SiteScreening module
    """

    def  __init__(self, methodName='runTest'):
        super(SiteDBTest, self).__init__(methodName=methodName, mockDBS=True, mockPhEDEx=True)

    def setUp(self):
        """
        Setup for unit tests
        """
        EmulatorHelper.setEmulators(phedex=False, dbs=False, siteDB=True, requestMgr=False)
        self.mySiteDB = SiteDBJSON()


    def tearDown(self):
        """
        _tearDown_
        """
        EmulatorHelper.resetEmulators()
        return


    def testCmsNametoPhEDExNode(self):
        """
        Tests CmsNametoSE
        """
        target = ['T1_US_FNAL_MSS','T1_US_FNAL_Buffer', 'T1_US_FNAL_Disk']
        results = self.mySiteDB.cmsNametoPhEDExNode("T1_US_FNAL")
        self.assertTrue(sorted(results) == sorted(target))
        
        target = ['T1_US_FNAL_Disk']
        results = [self.mySiteDB.cmsNametoPhEDExNode("T1_US_FNAL_Disk")]
        self.assertTrue(sorted(results) == sorted(target))

    def NtestCmsNametoSE(self):
        """
        Tests CmsNametoSE
        """
        target = [u'srm-cms-disk.gridpp.rl.ac.uk', u'srm-cms.gridpp.rl.ac.uk']
        results = self.mySiteDB.cmsNametoSE("T1_UK_RAL")
        self.assertTrue(sorted(results) == sorted(target))

    def NtestCmsNamePatterntoSE(self):
        """
        Tests CmsNamePatterntoSE
        """
        target = [u'srm-eoscms.cern.ch', u'srm-eoscms.cern.ch', u'storage01.lcg.cscs.ch', u'eoscmsftp.cern.ch']
        results = self.mySiteDB.cmsNametoSE("%T2_CH")
        print(target, results)
        self.assertTrue(sorted(results) == sorted(target))

    def NtestSEtoCmsName(self):
        """
        Tests CmsNametoSE
        """
        #pdb.set_trace()
        target = [u'T1_US_FNAL']
        results = self.mySiteDB.seToCMSName("cmssrm.fnal.gov")
        
        self.assertTrue(results == target)
        """ 
        target = sorted([u'T2_CH_CERN', u'T2_CH_CERN_HLT'])
        results = sorted(self.mySiteDB.seToCMSName("srm-eoscms.cern.ch"))
        self.assertTrue(sorted(results) == sorted(target))
        
        target = sorted([u'T0_CH_CERN', u'T1_CH_CERN'])
        results = sorted(self.mySiteDB.seToCMSName("srm-cms.cern.ch"))
        self.assertTrue(sorted(results) == sorted(target))
        
        target = sorted([u'T2_CH_CERN_AI'])
        results = sorted(self.mySiteDB.seToCMSName("eoscmsftp.cern.ch"))
        self.assertTrue(sorted(results) == sorted(target))
        """

    def NtestDNUserName(self):
        """
        Tests DN to Username lookup
        """
        testDn = "/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=gutsche/CN=582680/CN=Oliver Gutsche"
        testUserName = "gutsche"
        userName = self.mySiteDB.dnUserName(dn=testDn)
        self.assertTrue(testUserName == userName)

    def NtestDNWithApostrophe(self):
        """
        Tests a DN with an apostrophy in - will fail till SiteDB2 appears
        """
        testDn = "/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=liviof/CN=472739/CN=Livio Fano'"
        testUserName = "liviof"
        userName = self.mySiteDB.dnUserName(dn=testDn)
        self.assertTrue(testUserName == userName)

    def NtestSEFinder(self):
        """
        _testSEFinder_

        See if we can retrieve seNames from all sites
        """

        seNames = self.mySiteDB.getAllSENames()
        self.assertTrue(len(seNames) > 1)
        self.assertTrue('cmssrm.fnal.gov' in seNames)
        return

    def NtestPNNtoPSN(self):
        """
        _testPNNtoPSN_

        Test converting PhEDEx Node Name to Processing Site Name
        """

        result = self.mySiteDB.PNNtoPSN('T1_US_FNAL_Disk')
        self.assertTrue(result == ['T1_US_FNAL'])
        result = self.mySiteDB.PNNtoPSN('T1_US_FNAL_Tape')
        self.assertTrue(result == [])
        result = self.mySiteDB.PNNtoPSN('T2_UK_London_IC')
        self.assertTrue(result == ['T2_UK_London_IC'])
        return
    
    def NtestCMSNametoList(self):
        result = self.mySiteDB.cmsNametoList("T1_US*", "SE")
        self.assertItemsEqual(result, [u'cmssrm.fnal.gov', u'cmssrmdisk.fnal.gov'])

    def NtestCheckAndConvertSENameToPNN(self):
        """
        Test the conversion of SE name to PNN for single and multiple sites/PNNs using checkAndConvertSENameToPNN
        """

        fnalSE = u'cmssrm.fnal.gov'
        purdueSE = u'srm.rcac.purdue.edu'
        fnalPNNs = [u'T1_US_FNAL_Buffer', u'T1_US_FNAL_MSS']
        purduePNN = [u'T2_US_Purdue']

        pnnList = fnalPNNs + purduePNN
        seList = [fnalSE, purdueSE]

        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN(fnalSE), fnalPNNs)
        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN([fnalSE]), fnalPNNs)

        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN(purdueSE), purduePNN)
        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN([purdueSE]), purduePNN)

        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN(seList), purduePNN + fnalPNNs)

        self.assertItemsEqual(self.mySiteDB.checkAndConvertSENameToPNN(pnnList), pnnList)
        return


if __name__ == '__main__':
    unittest.main()
