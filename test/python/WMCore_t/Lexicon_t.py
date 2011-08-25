#!/usr/bin/python
"""
_Lexicon_t_

General test of Lexicon

"""

import logging
import unittest

from WMCore.Lexicon import *

class LexiconTest(unittest.TestCase):
    def testGoodSiteTier(self):
        # Check that valid tiers work
        assert sitetier('T0'), 'valid tier not validated'
        assert sitetier('T1'), 'valid tier not validated'
        assert sitetier('T2'), 'valid tier not validated'
        assert sitetier('T3'), 'valid tier not validated'

    def testBadSiteTier(self):
        # Check that invalid tiers raise an exception
        self.assertRaises(AssertionError, sitetier, 'T4')
        self.assertRaises(AssertionError, sitetier, 'D0')

    def testGoodJobranges(self):
        # Check that valid tiers work
        assert jobrange('3'), 'valid job range not validated'
        assert jobrange('78'), 'valid job range not validated'
        assert jobrange('3-9'), 'valid job range not validated'
        assert jobrange('32-97'), 'valid job range not validated'
        assert jobrange('2,3'), 'valid job range not validated'
        assert jobrange('24,39'), 'valid job range not validated'
        assert jobrange('2-91,45,5,64,7,78-91'), 'valid job range not validated'

    def testBadJobranges(self):
        # Check that invalid tiers raise an exception
        self.assertRaises(AssertionError, jobrange, 'I')
        self.assertRaises(AssertionError, jobrange, '1-2i')
        self.assertRaises(AssertionError, jobrange, '1-i2')
        self.assertRaises(AssertionError, jobrange, '1,2-3,3d-5')
        self.assertRaises(AssertionError, jobrange, '-1,2-3,3d-5')
        self.assertRaises(AssertionError, jobrange, '1-2,2,-5')

    def testGoodCMSName(self):
        # Check that full names work
        assert cmsname('T0_CH_CERN'), 'valid CMS name not validated'
        assert cmsname('T2_UK_SGrid_Bristol'), 'valid CMS name not validated'

    def testPartialCMSName(self):
        # Check that partial names work
        for i in ['T%', 'T2','T2_', 'T2_UK', 'T2_UK_', 'T2_UK_SGrid', 'T2_UK_SGrid_']:
            assert cmsname(i), 'partial CMS name (%s) not validated' % i

    def testBadCMSName(self):
        # Check that invalid names raise an exception
        self.assertRaises(AssertionError, cmsname, 'T5_UK_SGrid_Bristol')
        self.assertRaises(AssertionError, cmsname, 'T2-UK-SGrid_Bristol')
        self.assertRaises(AssertionError, cmsname, 'T2_UK_SGrid_Bris-tol')
        self.assertRaises(AssertionError, cmsname, 'D2_UK_SGrid_Bristol')
        self.assertRaises(AssertionError, cmsname, 'T2asjkjhadshjkdashjkasdkjhdas')
        #self.assertRaises(AssertionError, cmsname, 'T2_UK')

    def testGoodIdentifier(self):
        for ok in ['__wil.1.am__', '.']:
            assert identifier(ok)

    def testBadIdentifier(self):
        for notok in ['ke$ha', '<begin>']:
            self.assertRaises(AssertionError, identifier, notok)

    def testGoodDataset(self):
        assert dataset('/a/b/c')
        assert dataset('/m000n/RIII-ver/wider_than_1.0_miles')

    def testBadDataset(self):
        for notok in ['/Sugar/Sugar', '/Oh/honey/honey!', '/You/are/my/candy/GIIIRRL']:
           self.assertRaises(AssertionError, dataset, notok)

    def testVersion(self):
        for ok in ['CMSSW_3_8_0_pre1', 'CMSSW_1_2_0', 'CMSSW_4_0_0_patch11', 'CMSSW_3_10_0_pre9G493']:
            assert cmsswversion(ok)

    def testBadVersion(self):
        for notok in ['ORCA_3_8_0', 'CMSSW_3_5']:
            self.assertRaises(AssertionError, cmsswversion, notok)

    def testGoodCouchUrl(self):
        for ok in ['http://vittoria@antimatter.cern.ch:5984',
                   'https://fbi.fnal.gov:5984',
                   'http://fmulder:trustno1@fbi.fnal.gov:5984',
                   'http://localhost:443',
                   'http://127.0.0.1:1234',
                   'http://0.0.0.0:4321',
                   'http://1.2.3.4:5678',
                   'http://han:solo@1.2.3.4:9876',
                   'http://luke:skywalker@localhost:7654/some_db/some_doc',
                   'https://cmsreqmgr.cern.ch/couchdb/db1/doc' ]:
            assert couchurl(ok)

    def testBadCouchUrl(self):
        for notok in ['agent86@control.fnal.gov:5984', 'http:/localhost:443', 'http://www.myspace.com']:
            self.assertRaises(AssertionError, couchurl, notok)

    def testLFN(self):
        """
        _testLFN_

        Test the LFN checker in several modes, including user LFNs
        """

        lfnA = '/store/temp/user/ewv/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/temp/user/cinquilli.nocern/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/user/ewv/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/user/cinquilli.nocern/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/temp/group/Exotica/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/group/Exotica/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/temp1/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/temp/lustre1/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/backfill/1/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/data/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        lfn(lfnA)
        lfnA = '/store/data/Run2010A/Cosmics/RECO/v4/000/143/316/F65F4AFE-14AC-DF11-B3BE-00215E21F32E.root'
        lfn(lfnA)


        # All these cases should fail
        lfnA = '/storeA/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/Temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/Lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_;10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron;-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-rECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1;/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000a/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X;-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)


        # All these cases should fail
        lfnA = '/storeA/temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/Temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_;10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_10-A/MuElectron;-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_10-A/MuElectron-10_100/RAW-rECO/vX-1/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1;/1000/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000a/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X;-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)

        lfnA = '/store/temp/user/ewv/Higgs-123/PrivateSample/USER/v1/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/user/ewv/Higgs;123/PrivateSample/v1/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/user/ewv/Higgs-123/Private;Sample/v1/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/user/ewv/Higgs-123/PrivateSample/v1;/a_X-2.root'
        self.assertRaises(AssertionError, lfn, lfnA)

        return

    def testLFNBase(self):
        """
        _testLFNBase_

        Test the LFN Base
        """

        lfnA = '/store/temp/user/ewv/Higgs-123/PrivateSample/v1'
        lfnBase(lfnA)
        lfnA = '/store/user/ewv/Higgs-123/PrivateSample/v1'
        lfnBase(lfnA)
        lfnA = '/store/temp/group/Exotica/Higgs-123/PrivateSample/v1'
        lfnBase(lfnA)
        lfnA = '/store/user/group/Exotica/PrivateSample/v1'
        lfnBase(lfnA)
        lfnA = '/store/temp1/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        lfnBase(lfnA)
        lfnA = '/store/temp/lustre1/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        lfnBase(lfnA)

        lfnA = '/Store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/Temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/Lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition;_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10;_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-rECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX;-1'
        self.assertRaises(AssertionError, lfn, lfnA)


        lfnA = '/Store/temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/Temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition;_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_10-A/MuElectron-10;_100/RAW-RECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_10-A/MuElectron-10_100/RAW-rECO/vX-1'
        self.assertRaises(AssertionError, lfn, lfnA)
        lfnA = '/store/temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX;-1'
        self.assertRaises(AssertionError, lfn, lfnA)

        return


    def testLFNParser(self):
        """
        _testLFNParser_

        Check and make sure that we parse LFNs correctly
        """

        lfnA = '/store/temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        result = parseLFN(lfnA)

        self.assertEqual(result['baseLocation'], '/store/temp')
        self.assertEqual(result['acquisitionEra'], 'acquisition_10-A')
        self.assertEqual(result['primaryDataset'], 'MuElectron-10_100')
        self.assertEqual(result['dataTier'], 'RAW-RECO')
        self.assertEqual(result['processingVersion'], 'vX-1')
        self.assertEqual(result['lfnCounter'], '1000')
        self.assertEqual(result['filename'], 'a_X-2.root')

        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1/1000/a_X-2.root'
        result = parseLFN(lfnA)

        self.assertEqual(result['baseLocation'], '/store/temp/lustre')
        self.assertEqual(result['acquisitionEra'], 'acquisition_10-A')
        self.assertEqual(result['primaryDataset'], 'MuElectron-10_100')
        self.assertEqual(result['dataTier'], 'RAW-RECO')
        self.assertEqual(result['processingVersion'], 'vX-1')
        self.assertEqual(result['lfnCounter'], '1000')
        self.assertEqual(result['filename'], 'a_X-2.root')

        lfnA = '/store/temp/user/ewv/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        result = parseLFN(lfnA)

        self.assertEqual(result['baseLocation'], '/store/temp/user')
        self.assertEqual(result['primaryDataset'], 'Higgs-123')
        self.assertEqual(result['secondaryDataset'], 'PrivateSample')
        self.assertEqual(result['processingVersion'], 'v1')
        self.assertEqual(result['filename'], 'a_X-2.root')

        lfnA = '/store/user/ewv/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        result = parseLFN(lfnA)

        self.assertEqual(result['baseLocation'], '/store/user')
        self.assertEqual(result['primaryDataset'], 'Higgs-123')
        self.assertEqual(result['secondaryDataset'], 'PrivateSample')
        self.assertEqual(result['processingVersion'], 'v1')
        self.assertEqual(result['filename'], 'a_X-2.root')

        lfnA = '/store/group/Exotica/Higgs-123/PrivateSample/v1/1000/a_X-2.root'
        result = parseLFN(lfnA)

        self.assertEqual(result['baseLocation'], '/store/group')
        self.assertEqual(result['primaryDataset'], 'Higgs-123')
        self.assertEqual(result['secondaryDataset'], 'PrivateSample')
        self.assertEqual(result['processingVersion'], 'v1')
        self.assertEqual(result['filename'], 'a_X-2.root')

        return

    def testLFNBaseParser(self):
        """
        _testLFNBaseParser_

        Test the parsing for LFN Base
        """

        lfnA = '/store/temp/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        result = parseLFNBase(lfnA)

        self.assertEqual(result['baseLocation'], '/store/temp')
        self.assertEqual(result['acquisitionEra'], 'acquisition_10-A')
        self.assertEqual(result['primaryDataset'], 'MuElectron-10_100')
        self.assertEqual(result['dataTier'], 'RAW-RECO')
        self.assertEqual(result['processingVersion'], 'vX-1')

        lfnA = '/store/temp/lustre/acquisition_10-A/MuElectron-10_100/RAW-RECO/vX-1'
        result = parseLFNBase(lfnA)

        self.assertEqual(result['baseLocation'], '/store/temp/lustre')
        self.assertEqual(result['acquisitionEra'], 'acquisition_10-A')
        self.assertEqual(result['primaryDataset'], 'MuElectron-10_100')
        self.assertEqual(result['dataTier'], 'RAW-RECO')
        self.assertEqual(result['processingVersion'], 'vX-1')

        lfnA = '/store/temp/user/ewv/Higgs-123/PrivateSample/v1'
        result = parseLFNBase(lfnA)

        self.assertEqual(result['baseLocation'], '/store/temp/user')
        self.assertEqual(result['primaryDataset'], 'Higgs-123')
        self.assertEqual(result['secondaryDataset'], 'PrivateSample')
        self.assertEqual(result['processingVersion'], 'v1')

        lfnA = '/store/user/ewv/Higgs-123/PrivateSample/v1'
        result = parseLFNBase(lfnA)

        self.assertEqual(result['baseLocation'], '/store/user')
        self.assertEqual(result['primaryDataset'], 'Higgs-123')
        self.assertEqual(result['secondaryDataset'], 'PrivateSample')
        self.assertEqual(result['processingVersion'], 'v1')

        lfnA = '/store/group/Exotica/Higgs-123/PrivateSample/v1'
        result = parseLFNBase(lfnA)

        self.assertEqual(result['baseLocation'], '/store/group')
        self.assertEqual(result['primaryDataset'], 'Higgs-123')
        self.assertEqual(result['secondaryDataset'], 'PrivateSample')
        self.assertEqual(result['processingVersion'], 'v1')

        return

    def testSanitizeURL(self):
        proto = "http"
        host = "test.com"
        user = "abc"
        passwd = "^cba$"
        port  = "9999"
        url = "%s://%s:%s@%s:%s" % (proto, user, passwd, host, port)
        urlDict = sanitizeURL(url)
        self.assertEqual(urlDict['url'], "%s://%s:%s" % (proto, host, port))
        self.assertEqual(urlDict['username'], user)
        self.assertEqual(urlDict['password'], passwd)

        noPassURL = "http://test.com"
        urlDict = sanitizeURL(noPassURL)
        self.assertEqual(urlDict['url'], noPassURL)
        self.assertEqual(urlDict['username'], None)
        self.assertEqual(urlDict['password'], None)

if __name__ == "__main__":
    unittest.main()
