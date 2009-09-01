import sys
from Bio import SeqIO


READ_LENGTH = 75

average_array = [[0, 0, 0] for n in xrange(0, READ_LENGTH)]

for rec in SeqIO.parse(open(sys.argv[1]), "fastq-illumina"):
	for n in xrange(len(rec), 0, -1):
		rec = rec[0:n]
		average_array[n-1][0] = n
		average_array[n-1][1] += float(sum(rec.letter_annotations["phred_quality"])) / len(rec.letter_annotations["phred_quality"])
		average_array[n-1][2] += 1
		# print len(rec)

	#low_quality_bases = [x for x in rec.letter_annotations["phred_quality"] if x < 20]
	#if low_quality_bases:
	#	bad += 1
	#else:
	#	SeqIO.write([rec], sys.stdout, "fastq")
	#	good += 1
	#n += 1

	#SeqIO.write([rec], sys.stdout, "fastq")

for tup in average_array:
	print "%d : %s" % (tup[0], float(tup[1]) / tup[2])

# print >>sys.stderr, "good %d bad %d n %d" % (good, bad, n)

