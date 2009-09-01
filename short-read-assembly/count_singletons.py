import sys
from Bio import SeqIO

sequence_hash = {}
for rec in SeqIO.parse(open(sys.argv[1]), "fastq"):
	try:
		sequence_hash[rec.seq.tostring()] += 1
	except KeyError, e:
		sequence_hash[rec.seq.tostring()] = 1

num_hash = {}
for n in sequence_hash.values():
	try:
		num_hash[n] += 1
	except KeyError, e:
		num_hash[n] = 1

for k in sorted(num_hash.keys()):
	print "%d : %d" % (k, num_hash[k])

# print "good %d bad %d n %d" % (good, bad, n)

