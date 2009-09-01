import sys
from Bio import SeqIO

sequence_hash = {}

iter = SeqIO.parse(open(sys.argv[1]), "fastq")
try:
	while 1:
		rec1 = iter.next()
		rec2 = iter.next()

		if rec1.seq.tostring() in sequence_hash or rec2.seq.tostring() in sequence_hash:
			SeqIO.write([rec1, rec2], sys.stdout, "fastq")
			sequence_hash[rec1.seq.tostring()] = 1
			sequence_hash[rec1.seq.tostring()] = 1
		else:
			sequence_hash[rec1.seq.tostring()] = 1
			sequence_hash[rec2.seq.tostring()] = 1
except StopIteration:
	pass

