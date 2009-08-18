from Bio import SeqIO
import sys
import os

prefix = sys.argv[1]
fh = open("list", "w")
for rec in SeqIO.parse(open(prefix + ".gbk"), "genbank"):
	SeqIO.write([rec], open(rec.id, "w"), "genbank")
	print >>fh, rec.id
fh.close()

cmd = "/usr/local/bin/union -sequence @list -feature Y -source Y -outseq %s.temp -osformat2 genbank -sformat1 genbank" % (prefix)
print cmd
os.system(cmd)

fh = open(prefix + "_concat.gbk", "w")
for rec in SeqIO.parse(open(prefix + ".temp"), "genbank"):
	rec.id = prefix
	for f in rec.features:
		if f.type == 'source':
			f.type = 'contig'
			note = f.qualifiers['note'][0].replace('*origid: ', '')
			del f.qualifiers['note']
			f.qualifiers['label'] = [note]
	SeqIO.write([rec], fh, "genbank")
			
	

