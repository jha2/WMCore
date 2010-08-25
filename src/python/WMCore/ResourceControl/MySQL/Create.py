#!/usr/bin/python
"""
_Create_

Class for creating MySQL specific schema for resource control.
"""

__revision__ = "$Id: Create.py,v 1.3 2010/03/03 16:29:40 sfoulkes Exp $"
__version__ = "$Revision: 1.3 $"

import threading
from WMCore.Database.DBCreator import DBCreator

class Create(DBCreator):
    """
    _Create_
    
    Class for creating MySQL specific schema for resource control.
    """
    def __init__(self, logger = None, dbi = None, params = None):
        myThread = threading.currentThread()
        DBCreator.__init__(self, myThread.logger, myThread.dbi)
        self.create = {}
        self.constraints = {}

        self.create["rc_threshold"] = """
        CREATE TABLE rc_threshold(
            site_id INTEGER NOT NULL,
            sub_type_id INTEGER NOT NULL,
            min_slots INTEGER NOT NULL,
            max_slots INTEGER NOT NULL,
            FOREIGN KEY (site_id) REFERENCES wmbs_location(id) ON DELETE CASCADE,
            FOREIGN KEY (sub_type_id) REFERENCES wmbs_sub_types(id) ON DELETE CASCADE)"""

        return
