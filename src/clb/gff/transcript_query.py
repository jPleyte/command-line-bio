'''
Query the refseq gff for the cDNA transcript corresponding to a protein transcript or vis versa. 

Created on Dec 17, 2025

@author: pleyte
'''
import logging
import sys
import argparse
import gffutils
from dataclasses import dataclass
from tabulate import tabulate

@dataclass(frozen=True)
class Transcript:
    chrom: str
    cdna_transcript: str
    protein_transcript: str
    ccds: str
    gene: str    
    strand: str
        
class TranscriptQuery(object):
    '''
    Query a gff 
    '''
    def __init__(self, gff_db_filename):
        '''
        Constructor
        '''
        self._logger = logging.getLogger(__name__)
        self._logger.info("Reading GFF database " + gff_db_filename)
        self._gff_db = gffutils.FeatureDB(gff_db_filename)

    def query(self, transcript: str):        
        if transcript.startswith('NP'):
            return self._get_nm_using_np(transcript)
        elif transcript.startswith('NM'):
            return self._get_np_using_nm(transcript)
        else:
            raise ValueError(f"Unknown transcript type: {transcript}")
        

    def _get_nm_using_np(self, protein_transcript: str):
        '''
        Query the gff for the list of of cDNA transcripts associated with a protein transcript        
        '''
        query = """
                SELECT features.id 
                FROM features, json_each(features.attributes, '$.protein_id')
                WHERE json_each.value = ?
                """
        conn = self._gff_db.conn
        params = (protein_transcript,)
        cursor = conn.execute(query, params)
        transcripts = set()
        n_rows = 0
        for row in cursor:
            n_rows += 1
            feature = self._gff_db[row['id']]
            parent =  self._gff_db[feature.attributes['Parent'][0]]
            transcripts.add(self._get_transcript(feature, parent))

        self._logger.debug(f"Query for protein transcript {protein_transcript} returned {n_rows} rows  with {len(transcripts)} distinct transcripts.")

        if not transcripts:
            print(f"The protein transcript {protein_transcript} was not found in this gff")

        return transcripts

    def _get_np_using_nm(self, cdna_transcript):
        '''
        Query the gff for the protein transcript associated with the cDNA transcript 
        '''
        
        # Search mRNA features for the cdna transcript 
        nm_feature = None
        for feature in self._gff_db.features_of_type(['mRNA']):
            if 'Name' in feature.attributes and feature['Name'][0] == cdna_transcript:
                nm_feature = feature
                break
        
        transcripts = set()
        
        if not nm_feature:
            print(f"The cDNA transcript {cdna_transcript} was not found in this gff")
        else:
            # Search all children of the cdna feature to find the protein transcript  
            n_rows = 0
            for cds in self._gff_db.children(nm_feature, featuretype='CDS'):
                if 'protein_id' in cds.attributes:
                    n_rows += 1
                    transcripts.add(self._get_transcript(cds, nm_feature))

            self._logger.debug(f"Query for cDNA transcript {cdna_transcript} returned {n_rows} rows with {len(transcripts)} distinct transcript")
        
        return transcripts
            
            
    def _get_transcript(self, child_feature: gffutils.feature.Feature, parent_feature: gffutils.feature.Feature):
        '''
        '''
        ccds = self._get_ccds_accession(child_feature['Dbxref'])
        return Transcript(parent_feature.chrom, 
                          parent_feature.attributes['Name'][0], 
                          child_feature.attributes['Name'][0], 
                          ccds,
                          parent_feature.attributes['gene'][0], 
                          parent_feature.strand)
    
    def _get_ccds_accession(self, dbxrefs: list[str]):
        """
        Given a list of ids with the format "TYPE:ID" (eg CCDS:CCDS123.1) find the one with the prefix CCDS and return the id. 
        This is a helper function for modules that parse gffs using gffutils.    
        """        
        for acc in dbxrefs:
            if acc.startswith('CCDS:'):
                return acc.split(':')[1]
        
        return None

    def print(self, transcripts: list[Transcript]):
        '''
        '''
        headers = [ 'Chromosome', 'cDNA', 'Protein', 'CCDS', 'Gene', 'Strand' ]
        values_matrix = []
        
        for t in transcripts:
            row = [ t.chrom, t.cdna_transcript, t.protein_transcript, t.ccds, t.gene, t.strand ]
            values_matrix.append(row)
        
        print("")    
        print(tabulate(values_matrix, headers=headers))
        
def _parse_args():
    """
    Parse command line arguments 
    """
    parser = argparse.ArgumentParser(description='Query a GFF')

    parser.add_argument('--gff', help='A gff that has been converted to a gff utils db', required=True, type=str)
    parser.add_argument('transcript', help='The transcript to search for in the gff (eg NM_123.1 or NP_321.2', type=str)

    parser.add_argument("--version", action="version", version="clb-gff-t 0.0.2")
    return  parser.parse_args()

def main():
    # Setup logging to console
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)
    
    args = _parse_args()
    
    tq = TranscriptQuery(args.gff)
    
    transcripts = tq.query(args.transcript)
    
    tq.print(transcripts)
    
    
if __name__ == '__main__':
    main()
