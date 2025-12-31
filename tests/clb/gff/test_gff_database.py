'''
Created on Dec 30, 2025

@author: pleyte
'''
import unittest
import pathlib
from clb.gff.gff_database import GffDatabase
import tempfile
from pathlib import Path


class TestGffDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._test_data_dir = pathlib.Path(__file__).parent.parent.parent / "data"
        cls._tmp_dir = tempfile.TemporaryDirectory()
        cls._tiny_gff = cls._test_data_dir / "tiny.gff"
        
    # def setUp(self):
    #     """Runs before every test method."""
    #     x()
        
    @classmethod
    def tearDownClass(cls):
        """
        Runs after all tests are complete
        """
        cls._tmp_dir.cleanup()
    
    def test__create_db(self):
        """
        Convert a tiny gff from the test data directory to a db 
        """
        db_file = Path(self._tmp_dir.name) / "test.db"
        
        with GffDatabase(str(db_file), str(self._tiny_gff)) as db:
            self.assertIsNotNone(db, "The database object returned was None")
            self.assertTrue(Path(db.dbfn).exists(), "Database file was not created.")
            self.assertEqual(db.count_features_of_type('exon'), 2, "Exon count was not 2")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()