import sys
import tempfile
from Bio import SeqIO
import os

MUMMER_PATH = "/home/nick/bio/pkg/MUMmer3.21/"

if len(sys.argv) != 3:
	print "Usage: %s reference query" % (sys.argv[0])
	raise SystemExit


def ToFasta(fn):
	file = tempfile.NamedTemporaryFile()
	for rec in SeqIO.parse(open(fn), "genbank"):
		SeqIO.write([rec], file, "fasta")
	return file

file1 = ToFasta(sys.argv[1])
file2 = ToFasta(sys.argv[2])

prefix1 = os.path.split(sys.argv[1])[1]
prefix1 = os.path.splitext(prefix1)[0]

prefix2 = os.path.split(sys.argv[2])[1]
prefix2 = os.path.splitext(prefix2)[0]

prefix = "%s_%s" % (prefix1, prefix2)

cmd = "%s/nucmer --prefix=%s %s %s" % (MUMMER_PATH, prefix, file1.name, file2.name)
os.system(cmd)

cmd = "%s/show-coords -r %s.delta >%s.coords" % (MUMMER_PATH, prefix, prefix)
os.system(cmd)

fh = open("%s.coords" % (prefix))

outfh = open("%s.crunch" % (prefix), "w")

for ln in fh:
	if ln.startswith('='):
		break

for ln in fh:
	ln = ln.rstrip().replace('|', '')
	cols = ln.split()

	if int(cols[4]) > int(cols[5]):
		start = cols[4]
	else:
		start = cols[5]
	print >>outfh, "\t".join([
		cols[7],
		cols[8],
		cols[6],
		start,
		'#', '#',
		cols[2],
		cols[3],
		cols[0],
		cols[1],
		'#',
		cols[6]
	])

