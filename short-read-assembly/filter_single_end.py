import sys
from Bio import SeqIO

for rec in SeqIO.parse(open(sys.argv[1]), "fastq"):
	rec = rec[0:60]
	rec.id += '_long'
	if "N" in rec:
		continue
	low_quality_bases = [x for x in rec.letter_annotations["phred_quality"] if x < 20]
	if low_quality_bases:
		continue
	
	SeqIO.write([rec], sys.stdout, "fastq")

# print "good %d bad %d n %d" % (good, bad, n)

