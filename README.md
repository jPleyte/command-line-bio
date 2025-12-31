# command-line-bio

A command line tool for working with gff, fasta, and bioinformatics databases. 

## Installation

command-line-bio is hosted on TestPyPI, not PyPI, and is installed by running:
  
```sh
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ command-line-bio
```

## GFF Transcript Query

Retrieve information about transcripts from a gff. 
 
### Usage

Before you can query a gff you must first convert it to an SQLite database. This process takes a few minutes but only needs to be done once. 
  
```bash
$ clb gff createdb -gff /opt/GRCh37_latest_genomic.gff.gz --db /opt/GRCh37_latest_genomic.gff

Created /opt/GRCh37_latest_genomic.gff from /opt/GRCh37_latest_genomic.gff.gz
```

Lookup a cDNA transcript

```bash 
$ clb gff query --db /opt/GRCh37_latest_genomic.gff.db NM_001290187.2

Query for cDNA transcript NM_001290187.2 returned 18 rows with 1 distinct transcript

Chromosome    cDNA            Protein         CCDS         Gene    Strand
------------  --------------  --------------  -----------  ------  --------
NC_000007.13  NM_001290187.2  NP_001277116.1  CCDS78285.1  KRBA1   +
```

Lookup a protein transcript

```bash
$ clb gff query --db /opt/GRCh37_latest_genomic.gff.db NP_001034792.4

Query for protein transcript NP_001034792.4 returned 172 rows  with 2 distinct transcripts.

Chromosome      cDNA            Protein         CCDS    Gene    Strand
--------------  --------------  --------------  ------  ------  --------
NC_000001.10    NM_001039703.6  NP_001034792.4          NBPF10  +
NW_003871055.3  NM_001039703.6  NP_001034792.4          NBPF10  -
```

## Reference Query

Query reference genome. You can use a fasta file or [SeqRepo](https://github.com/biocommons/biocommons.seqrepo) installation as the reference source. 

### Usage

```bash
$ clb ref seq --fasta /opt/Homo_sapiens_assembly19.fasta chr1:111-121
$ clb ref seq --seqrepo /opt/seqrepo/latest chr1:111-121
```
