import sys, os
from Bio import SeqIO

if len(sys.argv) != 2:
	print "Usage: %s <prefix>" % (sys.argv[0])

prefix = sys.argv[1]
num = 1

for rec in SeqIO.parse(sys.stdin, "genbank"):
	for feat in rec.features:
		if feat.type == 'CDS':
			feat.qualifiers['locus_tag'] = ['%s%04d' % (prefix, num)]
			num += 1
	SeqIO.write([rec], sys.stdout, "genbank")

