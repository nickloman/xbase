import sys
from Bio import SeqIO

n = 0
bad = 0
good = 0

for rec in SeqIO.parse(open(sys.argv[1]), "fastq-illumina"):
	low_quality_bases = [x for x in rec.letter_annotations["phred_quality"] if x < 20]
	if low_quality_bases:
		bad += 1
	else:
		SeqIO.write([rec], sys.stdout, "fastq")
		good += 1
	n += 1

# print "good %d bad %d n %d" % (good, bad, n)

