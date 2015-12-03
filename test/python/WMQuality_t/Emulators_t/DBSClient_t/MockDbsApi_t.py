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
        self.mockDBS = MockDbsApi(self.endpoint)
        return

    def tearDown(self):
        return

    def testListDataTiers(self):
        """
        listDatatiers returns all datatiers available
        """
        #Get from  mock DBS
        results = self.mockDBS.listDataTiers()
        #assert the result
        self.assertNotEqual(results, None)
        data_tier_names = ['RAW', 'GEN-SIM-RECO', 'GEN-SIM']
        for result in results:
            self.assertTrue(result.has_key('data_tier_name'))
            self.assertTrue('RAW-ALAN' not in result['data_tier_name'])
        for tier in data_tier_names:
            self.assertTrue(tier in [result['data_tier_name']] for result in results)
        return

    def testListPrimaryDatasets(self):
        """
        listPrimaryDatasets returns known primary datasets
        """
        results = self.mockDBS.listPrimaryDatasets(primary_ds_name = 'Jet*')
        primary_ds_names = ['Jet', 'JetMET', 'JetMETTau']
        for name in primary_ds_names:
            self.assertTrue(name in [result['primary_ds_name']] for result in results)
        self.assertFalse(self.mockDBS.listPrimaryDatasets(primary_ds_name = 'DoesntExist'))
        return
    
    
    def testListRuns(self):
        """listRuns returns known runs"""
        runs = self.mockDBS.listRuns(dataset = DATASET)
        self.assertEqual(46, len(runs[0]['run_num']))
        self.assertTrue(174074 in runs[0]['run_num'])
        runs = self.mockDBS.listRuns(block_name = BLOCK)
        self.assertEqual(1, len(runs[0]['run_num']))
        self.assertEqual([173657], runs[0]['run_num'])


    def testlistDatasetFiles(self):
        """listDatasetFiles returns files in dataset"""
        files = self.mockDBS.listFileArray(dataset = DATASET)
        self.assertEqual(49, len(files))
        self.assertTrue(FILE in [f['logical_file_name']] for f in files)

    def testlistDatasetFileDetails(self):
        """testlistDatasetFilesDetails returns lumis, events, and parents of a dataset"""
        TESTFILE = '/store/data/Run2011A/HighPileUp/RAW/v1/000/173/658/56484BAB-CBCB-E011-AF00-BCAEC518FF56.root'
        details = self.mockDBS.listFileArray(dataset = DATASET, detail = True, validFileOnly = 1)
        self.assertEqual(len(details), 49)
        self.assertTrue(TESTFILE in [d['logical_file_name']] for d in details)
        self.assertTrue( 545 in [d['event_count']] for d in details )
#        self.assertEqual(details[TESTFILE]['file_size'], 286021145)
#        self.assertEqual(details[TESTFILE]['BlockName'], '/HighPileUp/Run2011A-v1/RAW#dd6e0796-cbcc-11e0-80a9-003048caaace')
#        self.assertEqual(details[TESTFILE]['Md5'], 'NOTSET')
#        self.assertEqual(details[TESTFILE]['md5'], 'NOTSET')
#        self.assertEqual(details[TESTFILE]['Adler32'], 'a41a1446')
#        self.assertEqual(details[TESTFILE]['adler32'], 'a41a1446')
#        self.assertEqual(details[TESTFILE]['Checksum'], '22218315')
#        self.assertEqual(details[TESTFILE]['check_sum'], '22218315')
#        self.assertTrue(173658 in details[TESTFILE]['Lumis'])
#        self.assertEqual(sorted(details[TESTFILE]['Lumis'][173658]),
#                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
#                          27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
#                          51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
#                          75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98,
#                          99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111])
#
#    def testGetDBSSummaryInfo(self):
#        """getDBSSummaryInfo returns summary of dataset and block"""
#        self.dbs = DBSReader(self.endpoint)
#        dataset = self.mockDBS.getDBSSummaryInfo(DATASET)
#        self.assertEqual(dataset['path'], DATASET)
#        self.assertEqual(dataset['block'], '')
#        self.assertEqual(dataset['NumberOfEvents'], 22075)
#        self.assertEqual(dataset['NumberOfBlocks'], 46)
#        self.assertEqual(dataset['FileSize'], 4001680824)
#        self.assertEqual(dataset['file_size'], 4001680824)
#        self.assertEqual(dataset['NumberOfFiles'], 49)
#        self.assertEqual(dataset['NumberOfLumis'], 7223)
#
#        block = self.mockDBS.getDBSSummaryInfo(DATASET, BLOCK)
#        self.assertEqual(block['path'], '')
#        self.assertEqual(block['block'], BLOCK)
#        self.assertEqual(block['NumberOfEvents'], 377)
#        self.assertEqual(block['NumberOfBlocks'], 1)
#        self.assertEqual(block['FileSize'], 150780132)
#        self.assertEqual(block['file_size'], 150780132)
#        self.assertEqual(block['NumberOfFiles'], 2)
#        self.assertEqual(block['NumberOfLumis'], 94)
#
#        self.assertRaises(DBSReaderError, self.mockDBS.getDBSSummaryInfo, DATASET + 'blah')
#        self.assertRaises(DBSReaderError, self.mockDBS.getDBSSummaryInfo, DATASET, BLOCK + 'asas')
#
#    @attr("integration")
#    def testGetFileBlocksInfo(self):
#        """getFileBlocksInfo returns block info, including location lookup"""
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

