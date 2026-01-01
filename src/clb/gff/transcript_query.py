'''
Query the refseq gff for the cDNA transcript corresponding to a protein transcript or vis versa. 

Created on Dec 17, 2025

@author: pleyte
'''
import logging
import gffutils
from dataclasses import dataclass, field
from tabulate import tabulate
from gffutils.interface import FeatureDB

@dataclass
class Transcript:
    chrom: str
    cdna_transcript: str
    gene: str    
    strand: str
    protein_transcript: str = None
    ccds: str = None
    exons: list = field(default_factory=list)
        
class TranscriptQuery(object):
    '''
    Query a gff 
    '''
    def __init__(self, feature_db: FeatureDB):
        '''
        Constructor
        '''
        self._logger = logging.getLogger(__name__)
        self._feature_db = feature_db

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
        conn = self._feature_db.conn
        params = (protein_transcript,)
        cursor = conn.execute(query, params)
        transcripts = set()
        n_rows = 0
        for row in cursor:
            n_rows += 1
            feature = self._feature_db[row['id']]
            parent =  self._feature_db[feature.attributes['Parent'][0]]
            transcripts.add(self._get_transcript(feature, parent))

        self._logger.debug(f"Query for protein transcript {protein_transcript} returned {n_rows} rows  with {len(transcripts)} distinct transcripts.")

        if not transcripts:
            print(f"The protein transcript {protein_transcript} was not found")

        return transcripts

    def _get_np_using_nm(self, cdna_transcript):
        '''
        Query the gff for the protein transcript associated with the cDNA transcript 
        '''
        # Search mRNA features for the cdna transcript 
        nm_feature = None
        for feature in self._feature_db.features_of_type(['mRNA']):
            if 'Name' in feature.attributes and feature['Name'][0] == cdna_transcript:
                nm_feature = feature
                break
        
        if not nm_feature:
            print(f"The cDNA transcript {cdna_transcript} was not found")
            return []
        else:
            # Search all children of the cdna feature to find the protein transcript  
            n_rows = 0
            
            transcript = Transcript(nm_feature.chrom, 
                                    nm_feature.attributes['Name'][0],
                                    nm_feature.attributes['gene'][0],
                                    nm_feature.strand)
            
            for cds in self._feature_db.children(nm_feature, featuretype='CDS'):
                n_rows += 1
                transcript.exons.append((cds.start, cds.end))

                if 'protein_id' in cds.attributes and transcript.protein_transcript is None:
                    transcript.protein_transcript = cds.attributes['Name'][0]

                if transcript.ccds is None:
                    transcript.ccds = self._get_ccds_accession(cds['Dbxref'])
                    
            self._logger.debug(f"Query for cDNA transcript {cdna_transcript} returned {n_rows} rows")
            return [transcript]
            
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
        
    def print_exons(self, exons: list[tuple], is_positive_strand):
        """
        """
        headers = [ 'Exon', 'Start', 'End' ]
        values_matrix = []
        n = 0
        for start, end in (sorted(exons) if is_positive_strand else sorted(exons, reverse=True)):            
            n += 1
            values_matrix.append([n, start, end])
        
        print("")
        print(tabulate(values_matrix, headers=headers))