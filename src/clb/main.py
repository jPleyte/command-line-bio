'''
Created on Dec 30, 2025

@author: pleyte
'''
import logging
import argparse
import sys
from clb.gff.gff_database import GffDatabase
from pathlib import Path
from clb.gff.transcript_query import TranscriptQuery

# Setup logging to console
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)
logger = logging.getLogger(__name__)

def _create_gff_db(args):
    """
    Takes an existing gff file and creates an SQLite database    
    """
    if not Path(args.gff).exists():
        raise ValueError(f"gff file does not exist: {args.gff}")
    elif Path(args.db).exists():
        raise ValueError(f"db file already exists: {args.db}")
    
    with GffDatabase(args.db, args.gff) as db:
        logger.info(f"Created {db.dbfn} from {args.gff}")
    
def _query_gff_db(args):
    """
    Takes a gff db and looks up transcript information  
    """
    with GffDatabase(args.db) as db:
        tq = TranscriptQuery(db)
        transcripts = tq.query(args.transcript)
        if transcripts: 
            tq.print(transcripts)
        
        if transcripts and args.exons:
            tq.print_exons(transcripts[0].exons, transcripts[0].strand == '+')
        
    
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
    create_gff_db_parser.set_defaults(func=lambda args: _create_gff_db(args))
    create_gff_db_parser.add_argument("--gff", help="GFF file to read", required=True)
    create_gff_db_parser.add_argument("--db", help="GFF database file to write", required=True)
    
    ## query gff database
    query_gff_parser = gff_subparsers.add_parser("query", help="Query gff")
    query_gff_parser.set_defaults(func=lambda args: _query_gff_db(args))
    query_gff_parser.add_argument("--db", help="GFF Database file", required=True)
    query_gff_parser.add_argument("--exons", help="Show exons", required=False, action='store_true')
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
    
    args = parser.parse_args()
    
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
        
    if hasattr(args, 'func'):
        args.func(args)

def main():
    _parse_args()

if __name__ == '__main__':
    main()
        