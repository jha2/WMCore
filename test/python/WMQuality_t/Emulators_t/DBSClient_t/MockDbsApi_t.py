#!/usr/bin/env python

import unittest
import mock
from nose.plugins.attrib import attr
from WMQuality.Emulators.DBSClient.MockDbsApi import MockDbsApi
from dbs.apis.dbsClient import DbsApi

# a small dataset that should always exist
DATASET = '/HighPileUp/Run2011A-v1/RAW'
BLOCK = '/HighPileUp/Run2011A-v1/RAW#fabf118a-cbbf-11e0-80a9-003048caaace'
file_names = [u'/store/data/Commissioning2015/Cosmics/RAW/v1/000/238/545/00000/C47FDF25-2ECF-E411-A8E2-02163E011839.root', u'/store/data/Commissioning2015/Cosmics/RAW/v1/000/238/545/00000/04FBE4D8-2DCF-E411-B827-02163E0124D5.root', u'/store/data/Commissioning2015/Cosmics/RAW/v1/000/238/545/00000/1043E89F-2DCF-E411-9CAE-02163E013751.root', u'/store/data/Commissioning2015/Cosmics/RAW/v1/000/238/545/00000/FA4E40C0-2DCF-E411-AD1A-02163E012186.root']


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

    def testDBSApiMembers(self):
        """
        Tests members from DBSApi
        """
        
        
        #List of members from DBSApi
        members = {'listDataTiers':{},
                'listDatasets':{'data_tier_name':'RAW', 'primary_ds_name':'Jet'},
                'listFileLumis':{'block_name':BLOCK, 'validFileOnly':1},
                'listFileLumiArray':{'logical_file_name': file_names},
                'listFileParents':{'block_name':'/Cosmics/Commissioning2015-PromptReco-v1/RECO#004ac3ba-d09e-11e4-afad-001e67ac06a0'},
                'listPrimaryDatasets':{'primary_ds_name':'Jet*'},
                'listRuns':{'dataset':DATASET},
                'listFileArray':{'dataset':DATASET},
                'listFileArray':{'dataset':DATASET, 'detail':True, 'validFileOnly':1},
                'listFileSummaries':{'dataset':DATASET, 'validFileOnly':1},
                'listBlocks':{'dataset':DATASET, 'detail':True},
                'listBlockParents':{'block_name' : '/Cosmics/Commissioning2015-PromptReco-v1/RECO#004ac3ba-d09e-11e4-afad-001e67ac06a0'},
               }
        
        for member in members.keys():
            #Get from  mock DBS
            args = []
            kwargs = members[member]

            real = getattr(self.realDBS, member)(*args, **kwargs)
            mock = getattr(self.mockDBS, member)(*args, **kwargs)
            
            #assert the result
            self.assertEqual(sorted(real), sorted(mock))

        return

if __name__ == '__main__':
    unittest.main()

