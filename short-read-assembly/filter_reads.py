import sys
from Bio import SeqIO

try:
    FILE_NAME = sys.argv[1]
    THRESHOLD = int(sys.argv[2])
except IndexError:
    print "Usage: filter_reads.py <fastq-file> <mean-quality-threshold>"
    raise SystemExit

iter = SeqIO.parse(open(sys.argv[1]), "fastq-illumina")
try:
    while 1:
        rec1 = iter.next()
        rec2 = iter.next()

        rec1_bad_bases = [x for x in rec1.letter_annotations["phred_quality"] if x < THRESHOLD]
        rec2_bad_bases = [x for x in rec2.letter_annotations["phred_quality"] if x < THRESHOLD]

        if not rec1_bad_bases and not rec2_bad_bases:
            SeqIO.write([rec1, rec2], sys.stdout, "fastq-illumina")
except StopIteration, e:
    pass


