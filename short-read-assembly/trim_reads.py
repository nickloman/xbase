import sys
from Bio import SeqIO

READ_LENGTH = 75
TRIM_LENGTH = 30

for rec in SeqIO.parse(open(sys.argv[1]), "fastq"):
	rec = rec[0:TRIM_LENGTH]
	SeqIO.write([rec], sys.stdout, "fastq")


