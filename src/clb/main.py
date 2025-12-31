'''
Created on Dec 30, 2025

@author: pleyte
'''
import logging
import argparse
import sys

def _parse_args():
    """
    Parse command line arguments 
    """
    parser = argparse.ArgumentParser(prog='clb', description='Query bioinformatics datasources from the command line')
    parser.add_argument("--version", action="version", version="clb 0.0.1")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # gff operations
    gff_parser = subparsers.add_parser("gff", help="GFF Operations")
    gff_subparsers = gff_parser.add_subparsers(dest="action")
    
    ## create gff database 
    create_gff_db_parser = gff_subparsers.add_parser("createdb", help="Create GFF database. This step must be performed before you can query the gff.")
    create_gff_db_parser.add_argument("--gff", help="GFF file to read", required=True)
    create_gff_db_parser.add_argument("--db", help="GFF database file to write", required=True)
    
    ## query gff database
    query_gff_parser = gff_subparsers.add_parser("query", help="Query gff")
    query_gff_parser.add_argument("--db", help="GFF Database file", required=True)
    query_gff_parser.add_argument("transcript", help="Transcript to lookup (eg NM_123.1 or NP_333.3)")
    
    # reference operations
    ref_parser = subparsers.add_parser("ref", help="Reference Operations")
    ref_subparsers = ref_parser.add_subparsers(dest="ref_action")
    
    ## get reference sequence 
    ref_sequence_parser = ref_subparsers.add_parser("seq", help="Get reference sequence")        
    ref_sequence_parser_group = ref_sequence_parser.add_mutually_exclusive_group(required=True)
    ref_sequence_parser_group.add_argument("--fasta", help="Reference FASTA file")
    ref_sequence_parser_group.add_argument("--seqrepo", help="SeqRepo installation directory")
    ref_sequence_parser.add_argument("coordinates", help="Coordinate range (eg chr3:111-122")
    
    return  parser.parse_args()

def main():
    # Setup logging to console
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)
    
    args = _parse_args()
    

if __name__ == '__main__':
    main()
        