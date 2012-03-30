#!/usr/bin/env python

"""
_scaleTest_

Fills a DBSBuffer with random data and then runs a DBSUpload process on it.
"""
import os
import sys
import time
import random
import logging
import threading

from WMCore.Services.UUID       import makeUUID
from WMQuality.TestInit         import TestInit
from WMCore.Agent.Configuration import Configuration
from WMCore.DAOFactory          import DAOFactory
from WMCore.DataStructs.Run     import Run

from WMComponent.DBS3Buffer.DBSBufferFile   import DBSBufferFile
from WMComponent.DBS3Buffer.DBSBufferUtil   import DBSBufferUtil
from WMComponent.DBS3Buffer.DBSUploadPoller import DBSUploadPoller

class scaleTestFiller:
    """
    _scaleTestFiller_

    Initializes the DB and the DBSUploader
    On __call__() it creates data and uploads it.
    """

    def __init__(self):
        """
        __init__

        Init the DB
        """

        self.testInit = TestInit(__file__)
        self.testInit.setLogging()
        self.testInit.setDatabaseConnection(destroyAllDatabase = True)
        self.testInit.setSchema(customModules = ["WMComponent.DBS3Buffer"],
                                useDefault = False)

        myThread = threading.currentThread()
        self.bufferFactory = DAOFactory(package = "WMComponent.DBSBuffer.Database",
                                        logger = myThread.logger,
                                        dbinterface = myThread.dbi)

        locationAction = self.bufferFactory(classname = "DBSBufferFiles.AddLocation")
        locationAction.execute(siteName = "se1.cern.ch")
        locationAction.execute(siteName = "se1.fnal.gov")
        locationAction.execute(siteName = "malpaquet")

        config = self.getConfig()
        self.dbsUploader = DBSUploadPoller(config = config)

        return


    def __call__(self):
        """
        __call__

        Generate some random data
        """

        # Generate somewhere between one and a thousand files
        name = "ThisIsATest_%s" % (makeUUID())
        nFiles = random.randint(10, 5000)
        name = name.replace('-', '_')
        name = '%s-v0' % name
        files = self.getFiles(name = name, nFiles = nFiles)

        print "Inserting %i files for dataset %s" % (nFiles, name)

        try:
            self.dbsUploader.algorithm()
        except:
            self.dbsUploader.close()
            raise

        # Repeat just to make sure
        try:
            self.dbsUploader.algorithm()
        except:
            self.dbsUploader.close()
            raise

        
        return
    


    def getConfig(self):
        """
        _getConfig_

        This creates the actual config file used by the component

        """


        config = Configuration()

        #First the general stuff
        config.section_("General")
        config.General.workDir = os.getenv("TESTDIR", os.getcwd())

        config.section_("Agent")
        config.Agent.componentName = 'DBSUpload'
        config.Agent.useHeartbeat  = False

        #Now the CoreDatabase information
        #This should be the dialect, dburl, etc
        config.section_("CoreDatabase")
        config.CoreDatabase.connectUrl = os.getenv("DATABASE")
        config.CoreDatabase.socket     = os.getenv("DBSOCK")


        config.component_("DBSUpload")
        config.DBSUpload.pollInterval     = 10
        config.DBSUpload.logLevel         = 'DEBUG'
        config.DBSUpload.DBSBlockMaxFiles = 500
        config.DBSUpload.DBSBlockMaxTime  = 600
        config.DBSUpload.DBSBlockMaxSize  = 999999999999
        config.DBSUpload.dbsUrl           = 'http://cms-xen40.fnal.gov:8787/dbs/prod/global/DBSWriter'
        config.DBSUpload.namespace        = 'WMComponent.DBS3Buffer.DBSUpload'
        config.DBSUpload.componentDir     = os.path.join(os.getcwd(), 'Components')
        config.DBSUpload.nProcesses       = 1
        config.DBSUpload.dbsWaitTime      = 1

        return config



    def getFiles(self, name, tier = 'RECO', nFiles = 12, site = "malpaquet", nLumis = 1):
        """
        Create some quick dummy test files

        """

        files = []

        for f in range(nFiles):
            testFile = DBSBufferFile(lfn = '/data/store/random/random/RANDOM/test/0/%s-%s-%i.root' % (name, site, f), size = 1024,
                                     events = 20, checksums = {'cksum': 1})
            testFile.setAlgorithm(appName = name, appVer = "CMSSW_3_1_1",
                                  appFam = "RECO", psetHash = "GIBBERISH",
                                  configContent = "MOREGIBBERISH")
            testFile.setDatasetPath("/%s/%s/%s" % (name, name, tier))
            lumis = []
            for i in range(nLumis):
                lumis.append((f * 100000) + i)
            testFile.addRun(Run( 1, *lumis))
            testFile.setAcquisitionEra(name.split('-')[0])
            testFile.setProcessingVer("0")
            testFile.setGlobalTag("Weird")
            testFile.create()
            testFile.setLocation(site)
            files.append(testFile)

        return files



if __name__ == "__main__":
    """
    Run the code

    """

    scaleTester = scaleTestFiller()

    while True:
        print "Ready to begin scale testing"
        scaleTester()
        print "Done running for now, sleeping temporarily"
        time.sleep(random.randint(10, 60))

