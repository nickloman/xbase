import sys
import os.path
from Bio import SeqIO

def get_name(name):
	head, tail = os.path.split(name)
	return tail.split(".")[0]

def link(fn, typ, d):
	head, tail = os.path.split(fn)
	prefix = tail.split(".")[0]
	str = "<a href=\"%s/%s.%s\">%s</a>" % (head, prefix, typ, d)
	return str

def collect_stats(fh):
	cds = 0
	tlen = 0
	records = 0
	recl = []
	for rec in SeqIO.parse(open(fh), "genbank"):
		records += 1
		cds += len([f for f in rec.features if f.type == 'CDS'])
		tlen += len(rec)
		recl.append(len(rec))
	recl.sort(reverse=True)
	total = 0 
	for n in recl:
		total += n
		if total > (tlen / 2):
			n50 = n
			break
	return [tlen, records, n50, cds]

print "sequence\ttotal length\tnum contigs\tn50\tnumber of predicted cds"
for arg in sys.argv[1:]:
	print get_name(arg), "\t",
	print link(arg, "fna", "FASTA"), "\t",
	print link(arg, "gbk", "GenBank"), "\t",
	print link(arg, "protein.faa", "Protein"), "\t",
	print "\t".join([str(a) for a in collect_stats(arg)])

