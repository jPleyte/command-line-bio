# command-line-bio

A command line tool for working with gff, fasta, and bioinformatics databases. 

## Installation

You can find the latest test release of command-line-bio on TestPyPI: https://test.pypi.org/project/command-line-bio/

To install from TestPyPI run
  
```bash
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            command-line-bio
```

## GFF Transcript Query

Retrieve information about transcripts from a gff. 
 
### Usage

Before you can query a gff you must first convert it to an SQLite database. This process takes a few minutes but only needs to be done once. 
  
```bash
$ clb gff createdb --gff /opt/GRCh37_latest_genomic.gff.gz --db /opt/GRCh37_latest_genomic.gff.db

Created /opt/GRCh37_latest_genomic.gff from /opt/GRCh37_latest_genomic.gff.gz
```


Lookup a cDNA transcript

```text
$ clb gff query --db /opt/GRCh37_latest_genomic.gff.db NM_001290187.2

Chromosome    cDNA            Protein         CCDS         Gene    Strand
------------  --------------  --------------  -----------  ------  --------
NC_000007.13  NM_001290187.2  NP_001277116.1  CCDS78285.1  KRBA1   +
```

Include exon positions by adding the ``--exons`` flag

```text
$ clb gff query --db /opt/GRCh37_latest_genomic.gff.db NM_000546.6 --exons

Chromosome    cDNA         Protein      CCDS         Gene    Strand
------------  -----------  -----------  -----------  ------  --------
NC_000017.10  NM_000546.6  NP_000537.3  CCDS11118.1  TP53    -

  Exon    Start      End
------  -------  -------
     1  7579839  7579912
     2  7579700  7579721
     3  7579312  7579590
     4  7578371  7578554
     5  7578177  7578289
     6  7577499  7577608
     7  7577019  7577155
     8  7576853  7576926
     9  7573927  7574033
    10  7572927  7573008
```

Lookup a protein transcript

```text
$ clb gff query --db /opt/GRCh37_latest_genomic.gff.db NP_001034792.4

Chromosome      cDNA            Protein         CCDS    Gene    Strand
--------------  --------------  --------------  ------  ------  --------
NC_000001.10    NM_001039703.6  NP_001034792.4          NBPF10  +
NW_003871055.3  NM_001039703.6  NP_001034792.4          NBPF10  -
```


## Reference Query

Query reference genome. You can use a fasta file or [SeqRepo](https://github.com/biocommons/biocommons.seqrepo) installation as the reference source. 

### Usage

```text
$ clb ref seq --fasta /opt/Homo_sapiens_assembly19.fasta chr1:111-121
$ clb ref seq --seqrepo /opt/seqrepo/latest chr1:111-121
```
