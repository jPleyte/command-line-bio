# command-line-bio
Command line tools for working with gff, fasta, and bioinformatics databases. 

## GFF Transcript Query (clb.gff.transcript_query)

Retrieve information about transcripts from a gff. 
 
### Usage

```sh
export PYTHONPATH=$PYTHONPATH:~/git/command-line-bio/src
python -m clb.gff.transcript_query --gff /opt/bioinformatics/ncbi/GRCh37_latest_genomic.gff.db NM_001290187.2
python -m clb.gff.transcript_query --gff /opt/bioinformatics/ncbi/GRCh37_latest_genomic.gff.db NP_001277116.1
```
