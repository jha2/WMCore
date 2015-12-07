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

#    def testGetFileBlocksInfo(self):
#        """getFileBlocksInfo returns block info, including location lookup"""
#        # results = self.realDBS.getFileBlocksInfo(dataset = DATASET) 
#        mock = self.mockDBS.getFileBlocksInfo(dataset = DATASET)
#        print "real: %s" %results
        
        #assert the result
        #self.assertEqual(sorted(results), sorted(mock))
#        self.dbs = DBSReader(self.endpoint)
#        blocks = self.mockDBS.getFileBlocksInfo(DATASET)
#        block = self.mockDBS.getFileBlocksInfo(DATASET, blockName=BLOCK)
#        self.assertEqual(1, len(block))
#        block = block[0]
#        self.assertEqual(46, len(blocks))
#        self.assertTrue(block['Name'] in [x['Name'] for x in blocks])
#        self.assertEqual(BLOCK, block['Name'])
#        self.assertEqual(0, block['OpenForWriting'])
#        self.assertEqual(150780132, block['BlockSize'])
#        self.assertEqual(2, block['NumberOfFiles'])
#        # possibly fragile but assume block located at least at cern
#        sites = [x['Name'] for x in block['PhEDExNodeList'] if x['Name'].find('CH_CERN') > -1]
#        self.assertTrue(sites)
#
#        # weird error handling - depends on whether block or dataset is missing
#        self.assertRaises(DBSReaderError, self.mockDBS.getFileBlocksInfo, DATASET + 'blah')
#        self.assertRaises(DBSReaderError, self.mockDBS.getFileBlocksInfo, DATASET, blockName=BLOCK + 'asas')
#
#    def testListFileBlocks(self):
#        """listFileBlocks returns block names in dataset"""
#        self.dbs = DBSReader(self.endpoint)
#        blocks = self.mockDBS.listFileBlocks(DATASET)
#        self.assertTrue(BLOCK in blocks)
#        # block is closed
#        block = self.mockDBS.listFileBlocks(DATASET, blockName=BLOCK, onlyClosedBlocks=True)[0]
#        self.assertEqual(block, BLOCK)
#        self.assertTrue(BLOCK in block)
#
#    def testListOpenFileBlocks(self):
#        """listOpenFileBlocks finds open blocks"""
#        # hard to find a dataset with open blocks, so don't bother
#        self.dbs = DBSReader(self.endpoint)
#        self.assertFalse(self.mockDBS.listOpenFileBlocks(DATASET))
#
#    def testBlockExists(self):
#        """blockExists returns existence of blocks"""
#        self.dbs = DBSReader(self.endpoint)
#        self.assertTrue(self.mockDBS.blockExists(BLOCK))
#        self.assertRaises(DBSReaderError, self.mockDBS.blockExists, DATASET + '#somethingelse')
#
#    def testListFilesInBlock(self):
#        """listFilesInBlock returns files in block"""
#        self.dbs = DBSReader(self.endpoint)
#        self.assertTrue(FILE in [x['LogicalFileName'] for x in self.mockDBS.listFilesInBlock(BLOCK)])
#        self.assertRaises(DBSReaderError, self.mockDBS.listFilesInBlock, DATASET + '#blah')



if __name__ == '__main__':
    unittest.main()

