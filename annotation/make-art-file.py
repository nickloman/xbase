#!/usr/bin/python

from Bio import SeqIO
import sys
import os
from tempfile import NamedTemporaryFile

prefix = sys.argv[1]

list_file = NamedTemporaryFile(delete=False)
for rec in SeqIO.parse(sys.stdin, "genbank"):
    t = NamedTemporaryFile(delete=False)
    SeqIO.write([rec], t, "genbank")
    print >>list_file, t.name
list_file.close()

temp_genbank_file = NamedTemporaryFile(delete=False)
temp_genbank_file.close()

cmd = "/usr/local/bin/union -sequence @%s -feature Y -source Y -outseq %s -osformat2 genbank -sformat1 genbank"% (list_file.name, temp_genbank_file.name)
print >>sys.stderr, cmd
os.system(cmd)

for rec in SeqIO.parse(open(temp_genbank_file.name), "genbank"):
    rec.id = prefix
    for f in rec.features:
        if f.type == 'source':
            f.type = 'contig'
            note = f.qualifiers['note'][0].replace('*origid: ', '')
            del f.qualifiers['note']
            f.qualifiers['label'] = [note]
    SeqIO.write([rec], sys.stdout, "genbank")
            
    

