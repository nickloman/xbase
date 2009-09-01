#!/usr/bin/python

import sys
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
from operator import attrgetter

class tRNA:
    def __init__(self, cols):
        self.rec_id = cols[0]
        self.id = cols[1]
        self.start = int(cols[2])
        self.end = int(cols[3])
        self.amino_acid = cols[4]
        self.anticodon = cols[5]
        self.cove_score = cols[8]

def convert_trna_feature(trna):
    if trna.start < trna.end:
        return FeatureLocation(rna.start - 1, rna.end), 1
    else:
        return FeatureLocation(rna.end - 1, rna.start), -1

def location_sort(a, b):
    return cmp(a.location.nofuzzy_start, b.location.nofuzzy_end)

if len(sys.argv) != 3:
    print "Usage: find_trna.py <genbank file> <trnascan output>"
    raise SystemExit

trna_list = []
fh = open(sys.argv[2])
itr = fh.__iter__()
itr.next()
itr.next()
itr.next()
for ln in fh:
    cols = [col.strip() for col in ln.rstrip().split("\t")]
    trna_list.append(tRNA(cols))

for rec in SeqIO.parse(open(sys.argv[1]), "genbank"):
    for rna in trna_list:
        if rna.rec_id == rec.id:
            location, strand = convert_trna_feature(rna)
            qualifiers = {}
            qualifiers['locus_tag'] = ['tRNA-%s' % (rna.id,)]
            qualifiers['product'] = ['tRNA-%s' % (rna.amino_acid)]
            qualifiers['note'] = ['tRNA predicted by tRNAScan-SE anticodon %s cove score %s' % (rna.anticodon, rna.cove_score)]
            rec.features.append(SeqFeature(type='tRNA', location=location, strand=strand, qualifiers=qualifiers))            
    rec.features.sort(location_sort)
    SeqIO.write([rec], sys.stdout, "genbank")

