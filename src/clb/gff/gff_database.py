'''
Created on Dec 30, 2025

@author: pleyte
'''

import logging
import gffutils
from gffutils.interface import FeatureDB
from pathlib import Path

class GffDatabase(object):
    '''
    classdocs
    '''
    def __init__(self, db_file: str, gff_file: str = None):
        '''
        Pass the optional gff parameter to convert the gff to an SQLite db.   
        '''
        self._logger = logging.getLogger(__name__)
        self._db_file = db_file
        self._gff_file = gff_file
        self._db = None
    
    def _create_db(self):
        """
        Use gffutils to convert a gff to SQLite db. 
        """
        self._logger.debug(f"Creating SQLite database {self._db_file} from GFF file {self._gff_file}")
        self._db = gffutils.create_db(self._gff_file, self._db_file, merge_strategy='create_unique', verbose = True)
        
    def _open_db(self):
        """
        Open the SQLite db 
        """
        self._db = gffutils.FeatureDB(self._db_file)
        
    def __enter__(self) -> FeatureDB:
        """
        Open and return the gff database 
        """
        if not Path(self._db_file).exists():
            self._create_db()
        else:
            self._open_db()
        
        return self._db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures the database connection is closed when exiting the 'with' block.
        """
        if self._db:
            self._db.conn.close()
