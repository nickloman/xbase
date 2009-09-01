#!/usr/bin/python

import sys
from Bio import SeqIO

if __name__ == '__main__':
    average_array = None
    first_run = True

    try:
        file_name = sys.argv[1]
    except IndexError, e:
        print "Usage: quality_breakdown.py <fastq-file>"
        raise SystemExit

    for rec in SeqIO.parse(open(sys.argv[1]), "fastq-illumina"):
        if first_run:
            average_array = [[0, 0, 0] for n in xrange(0, len(rec))]
            first_run = False
	    for n in xrange(len(rec), 0, -1):
		    rec = rec[0:n]
		    average_array[n-1][0] = n
		    average_array[n-1][1] += float(sum(rec.letter_annotations["phred_quality"])) / len(rec.letter_annotations["phred_quality"])
		    average_array[n-1][2] += 1

    print "base\tmean_quality"
    for tup in average_array:
	    print "%d\t%s" % (tup[0], float(tup[1]) / tup[2])

