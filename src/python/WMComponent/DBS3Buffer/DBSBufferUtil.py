#!/usr/bin/env python
"""
_DBSBufferUtil_

APIs related to using the DBSBuffer.
"""

import threading

from WMCore.DAOFactory import DAOFactory
from WMComponent.DBS3Buffer.DBSBufferFile import DBSBufferFile
from WMCore.DataStructs.Run import Run
from WMCore.WMConnectionBase import WMConnectionBase

class DBSBufferUtil(WMConnectionBase):
    """
    APIs related to file addition for DBSBuffer

    """
    def __init__(self):

        myThread = threading.currentThread()
        self.daoFactory = DAOFactory(package = "WMComponent.DBS3Buffer",
                                     logger = myThread.logger,
                                     dbinterface = myThread.dbi)

<<<<<<< HEAD

    def addFile(self, file, dataset=0):
        """
        Add the file to the buffer
        """

        myThread = threading.currentThread()

        existingTransaction = self.beginTransaction()

        bufferFile = DBSBufferFile(lfn = file['LFN'], size = file['Size'],
                                   events = file['TotalEvents'],
                                   cksum=file['Checksum'], dataset=dataset)

        runLumiList = file.getLumiSections()
        runList     = [x['RunNumber'] for x in runLumiList]

        for runNumber in runList:
            lumis = [int(y['LumiSectionNumber']) for y in runLumiList if y['RunNumber']==runNumber]
            run=Run(runNumber, *lumis)
            bufferFile.addRun(run)

        if bufferFile.exists() == False:
            bufferFile.create()
            bufferFile.setLocation(pnn=file['locations'], immediateSave = True)
        else:
            bufferFile.load()
        # Lets add the file to DBS Buffer as well
        #UPDATE File Count

        self.updateDSFileCount(dataset=dataset)

        #Parent files
        bufferFile.addParents(file.inputFiles)

        self.commitTransaction(existingTransaction)

        return


    def addDataset(self, dataset, algoInDBS):
        """
        Add the dataset to the buffer (API Call)
        """
        myThread = threading.currentThread()

        existingTransaction = self.beginTransaction()

        newDS = self.daoFactory(classname = "NewDataset")
        newDS.execute(datasetPath=dataset["Path"], conn = self.getDBConn(), transaction=self.existingTransaction())

        self.commitTransaction(existingTransaction)
        return

    def addAlgo(self, algo):
        """
        Add the algo to the buffer (API Call)
        dataset object contains the algo information
        """
        myThread = threading.currentThread()

        existingTransaction = self.beginTransaction()

        newDS = self.daoFactory(classname = "NewAlgo")
        newDS.execute(appName = algo["ApplicationName"], appVer = algo["ApplicationVersion"], appFam = algo["ApplicationName"], \
                      psetHash = algo["PSetHash"], configContent = algo["PSetContent"], \
                      conn = self.getDBConn(), transaction=self.existingTransaction())
        self.commitTransaction(existingTransaction)
        return

    def updateDSFileCount(self, dataset):
        """
        _updateDSFileCount_

        Update a dataset with its files
        """

        existingTransaction = self.beginTransaction()

        newDS = self.daoFactory(classname = "UpdateDSFileCount")
        newDS.execute(dataset=dataset, conn = self.getDBConn(), transaction=self.existingTransaction())
        self.commitTransaction(existingTransaction)
        return


    def updateAlgo(self, algo, inDBS = 0):
        """
        Update the algo with inDBS information
        """
        myThread = threading.currentThread()

        existingTransaction = self.beginTransaction()

        newDS = self.daoFactory(classname = "UpdateAlgo")
        newDS.execute(inDBS = inDBS, appName = algo["ApplicationName"], appVer = algo["ApplicationVersion"], appFam = algo["ApplicationFamily"], \
                      psetHash = algo["PSetHash"], conn = self.getDBConn(), transaction=self.existingTransaction())
        self.commitTransaction(existingTransaction)
=======
>>>>>>> df87295b4f5ba433a5e722c0e60675dc3ef1e16b
        return


    def loadDBSBufferFilesBulk(self, fileObjs):
        """
        _loadDBSBufferFilesBulk_

        Yes, this is a stupid place to put it.
        No, there's not better place.
        """
        dbsFiles = []

        binds = []
        for f in fileObjs:
            binds.append(f["id"])

        loadFiles = self.daoFactory(classname = "DBSBufferFiles.LoadBulkFilesByID")
        results = loadFiles.execute(files = binds, transaction = False)

        for entry in results:
            # Add loaded information
            dbsfile = DBSBufferFile(id=entry['id'])
            dbsfile.update(entry)
            dbsFiles.append(dbsfile)

        for dbsfile in dbsFiles:
            if 'runInfo' in dbsfile.keys():
            # Then we have to replace it with a real run
                for r in dbsfile['runInfo'].keys():
                    run = Run(runNumber = r)
                    run.extend(dbsfile['runInfo'][r])
                    dbsfile.addRun(run)
                del dbsfile['runInfo']
            if 'parentLFNs' in dbsfile.keys():
                # Then we have some parents
                for lfn in dbsfile['parentLFNs']:
                    newFile = DBSBufferFile(lfn = lfn)
                    dbsfile['parents'].add(newFile)
                del dbsfile['parentLFNs']

        return dbsFiles


    def findUploadableDAS(self):
        """
        _findUploadableDAS_

        Find all dataset_algo with uploadable files.
        """
        findDAS = self.daoFactory(classname = "FindDASToUpload")
        result = findDAS.execute(transaction = False)

        return result


    def findOpenBlocks(self):
        """
        _findOpenBlocks_

        This should find all blocks.
        """
        openBlocks = self.daoFactory(classname = "GetOpenBlocks")
        result = openBlocks.execute(transaction = False)

        return result


    def loadBlocksByDAS(self, das):
        """
        _loadBlocksByDAS_

        Given a DAS, find all the
        blocks associated with it in the
        Open status
        """
        findBlocks = self.daoFactory(classname = "LoadBlocksByDAS")
        result = findBlocks.execute(das = das, transaction = False)

        return result


    def loadBlocks(self, blocknames):
        """
        _loadBlocks_

        Given a list of names, load the
        blocks with those names
        """

        if len(blocknames) < 1:
            # Nothing to do
            return []

        findBlocks = self.daoFactory(classname = "LoadBlocks")
        result = findBlocks.execute(blocknames, transaction = False)

        return result


    def findUploadableFilesByDAS(self, datasetpath):
        """
        _findUploadableDAS_

        Find all the uploadable files for a given DatasetPath.
        """
        dbsFiles = []

        findFiles = self.daoFactory(classname = "LoadDBSFilesByDAS")
        results = findFiles.execute(datasetpath = datasetpath, transaction = False)

        for entry in results:
            # Add loaded information
            dbsfile = DBSBufferFile(id=entry['id'])
            dbsfile.update(entry)
            dbsFiles.append(dbsfile)

        for dbsfile in dbsFiles:
            if 'runInfo' in dbsfile.keys():
                # Then we have to replace it with a real run
                for r in dbsfile['runInfo'].keys():
                    run = Run(runNumber = r)
                    run.extend(dbsfile['runInfo'][r])
                    dbsfile.addRun(run)
                del dbsfile['runInfo']
            if 'parentLFNs' in dbsfile.keys():
                # Then we have some parents
                for lfn in dbsfile['parentLFNs']:
                    newFile = DBSBufferFile(lfn = lfn)
                    dbsfile['parents'].add(newFile)
                del dbsfile['parentLFNs']

        return dbsFiles


    def loadFilesByBlock(self, blockname):
        """
        _loadFilesByBlock_

        Get all files associated with a block
        """
        dbsFiles = []

        findFiles = self.daoFactory(classname = "LoadFilesByBlock")
        results = findFiles.execute(blockname = blockname, transaction = False)

        for entry in results:
            # Add loaded information
            dbsfile = DBSBufferFile(id=entry['id'])
            dbsfile.update(entry)
            dbsFiles.append(dbsfile)

        for dbsfile in dbsFiles:
            if 'runInfo' in dbsfile.keys():
                # Then we have to replace it with a real run
                for r in dbsfile['runInfo'].keys():
                    run = Run(runNumber = r)
                    run.extend(dbsfile['runInfo'][r])
                    dbsfile.addRun(run)
                del dbsfile['runInfo']
            if 'parentLFNs' in dbsfile.keys():
                # Then we have some parents
                for lfn in dbsfile['parentLFNs']:
                    newFile = DBSBufferFile(lfn = lfn)
                    dbsfile['parents'].add(newFile)
                del dbsfile['parentLFNs']

        return dbsFiles
    
    
    def getCompletedWorkflows(self):
        """
        _getCompletedWorkflows_

        """
        wfCompletedDAO = self.daoFactory(classname = "GetCompletedWorkflows")
        result = wfCompletedDAO.execute(transaction = False)

        return result
