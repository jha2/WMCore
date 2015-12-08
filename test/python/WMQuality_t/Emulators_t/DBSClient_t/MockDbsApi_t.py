#!/usr/bin/env python

import unittest
import mock
from nose.plugins.attrib import attr
from WMQuality.Emulators.DBSClient.MockDbsApi import MockDbsApi
from dbs.apis.dbsClient import DbsApi

# a small dataset that should always exist
DATASET = '/HighPileUp/Run2011A-v1/RAW'
BLOCK = '/HighPileUp/Run2011A-v1/RAW#fabf118a-cbbf-11e0-80a9-003048caaace'
FILE = '/store/data/Run2011A/HighPileUp/RAW/v1/000/173/657/B293AF24-BFCB-E011-8F85-BCAEC5329701.root'


class MockDbsApiTest(unittest.TestCase):
    """
    Class that can be imported to switch to 'mock'ed versions of
    services.

    """

    def setUp(self):
        self.endpoint = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader'
        self.realDBS = DbsApi(self.endpoint)
        self.mockDBS = MockDbsApi(self.endpoint)
        return

    def tearDown(self):
        return

    def testListDataTiers(self):
        """
        listDatatiers returns all datatiers available
        """
        #Get from  mock DBS
        mock = self.mockDBS.listDataTiers()
        results = self.realDBS.listDataTiers()
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return

    def testListDatasets(self):
        """
        listDatasets returns known  datasets for a given data_tier_name and primary ds
        """
        results = self.realDBS.listDatasets(data_tier_name = 'RAW', primary_ds_name = 'Jet') 
        mock = self.mockDBS.listDatasets(data_tier_name = 'RAW', primary_ds_name = 'Jet')
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return
    
    def testListFileLumis(self):
        """
        listFileLumis returns known lumi sections  for a given  block
        """
        results = self.realDBS.listFileLumis(block_name = BLOCK, validFileOnly = 1) 
        mock = self.mockDBS.listFileLumis(block_name = BLOCK, validFileOnly = 1) 
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return
    
    def testListFileLumiArray(self):
        """
        listFileLumiArray returns known lumi sections  for a given list of files
        """
        file_names = [u'/store/data/Commissioning2015/Cosmics/RAW/v1/000/238/545/00000/C47FDF25-2ECF-E411-A8E2-02163E011839.root', u'/store/data/Commissioning2015/Cosmics/RAW/v1/000/238/545/00000/04FBE4D8-2DCF-E411-B827-02163E0124D5.root', u'/store/data/Commissioning2015/Cosmics/RAW/v1/000/238/545/00000/1043E89F-2DCF-E411-9CAE-02163E013751.root', u'/store/data/Commissioning2015/Cosmics/RAW/v1/000/238/545/00000/FA4E40C0-2DCF-E411-AD1A-02163E012186.root']
        results = self.realDBS.listFileLumiArray(logical_file_name = file_names) 
        mock = self.mockDBS.listFileLumiArray(logical_file_name = file_names) 
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return
    
    def testlistFileParents(self):
        """listFileParents returns parent logical and logical file names  in a block"""
        results = self.realDBS.listFileParents(block_name = "/Cosmics/Commissioning2015-PromptReco-v1/RECO#004ac3ba-d09e-11e4-afad-001e67ac06a0") 
        mock = self.mockDBS.listFileParents(block_name = "/Cosmics/Commissioning2015-PromptReco-v1/RECO#004ac3ba-d09e-11e4-afad-001e67ac06a0") 
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return 
        
    def testListPrimaryDatasets(self):
        """
        listPrimaryDatasets returns known primary datasets
        """
        results = self.realDBS.listPrimaryDatasets(primary_ds_name = 'Jet*') 
        mock = self.mockDBS.listPrimaryDatasets(primary_ds_name = 'Jet*')
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return
    
    
    def testListRuns(self):
        """listRuns returns known runs"""
        results = self.realDBS.listRuns(dataset = DATASET) 
        mock = self.mockDBS.listRuns(dataset = DATASET)
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return
        


    def testlistDatasetFiles(self):
        """listDatasetFiles returns files in dataset"""
        results = self.realDBS.listFileArray(dataset = DATASET) 
        mock = self.mockDBS.listFileArray(dataset = DATASET)
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return 
        

    def testlistDatasetFileDetails(self):
        """testlistDatasetFilesDetails returns lumis, events, and parents of a dataset"""
        TESTFILE = '/store/data/Run2011A/HighPileUp/RAW/v1/000/173/658/56484BAB-CBCB-E011-AF00-BCAEC518FF56.root'
        results = self.realDBS.listFileArray(dataset = DATASET, detail = True, validFileOnly = 1) 
        mock = self.mockDBS.listFileArray(dataset = DATASET, detail = True, validFileOnly = 1)
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return

    def testGetDBSSummaryInfo(self):
        """getDBSSummaryInfo returns summary of dataset and block"""
        results = self.realDBS.listFileSummaries(dataset = DATASET, validFileOnly = 1) 
        mock = self.mockDBS.listFileSummaries(dataset = DATASET, validFileOnly = 1)
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))
        return

    def testGetFileBlocksInfo(self):
        """getFileBlocksInfo returns block info, including location lookup"""
        results = self.realDBS.listBlocks(dataset = DATASET, detail = True) 
        mock = self.mockDBS.listBlocks(dataset = DATASET, detail = True) 
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))

    def testListFilesInBlockWithParents(self):
        """ get parents for a block"""
        results = self.realDBS.listBlockParents(block_name = '/Cosmics/Commissioning2015-PromptReco-v1/RECO#004ac3ba-d09e-11e4-afad-001e67ac06a0')
        mock = self.mockDBS.listBlockParents(block_name = '/Cosmics/Commissioning2015-PromptReco-v1/RECO#004ac3ba-d09e-11e4-afad-001e67ac06a0')
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))

        """gets files with parents for a block"""
        results = self.realDBS.listFileArray(block_name = '/Cosmics/Commissioning2015-PromptReco-v1/RECO#004ac3ba-d09e-11e4-afad-001e67ac06a0', detail = True, validFileOnly = 1)
        mock = self.mockDBS.listFileArray(block_name = '/Cosmics/Commissioning2015-PromptReco-v1/RECO#004ac3ba-d09e-11e4-afad-001e67ac06a0', detail = True, validFileOnly = 1)
        #assert the result
        self.assertEqual(sorted(results), sorted(mock))

if __name__ == '__main__':
    unittest.main()

