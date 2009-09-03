#!/usr/bin/python

import sys, os
import sets
from Bio import SeqIO

def make_location_set(l):
    return sets.Set([n for n in xrange(l.nofuzzy_start, l.nofuzzy_end)])

for rec in SeqIO.parse(sys.stdin, "genbank"):
    new_features = []
    for feature in rec.features:
        add = 1
        if feature.type == 'CDS':
            if '*' in feature.qualifiers['translation'][0]:
                location_set = make_location_set(feature.location)

                for f2 in rec.features:
                    if f2.type == 'CDS' and f2 != feature:
                        ret = location_set.intersection(make_location_set(f2.location))
                        if ret:
                            add = 0
        if add:
            new_features.append(feature)

    rec.features = new_features
    SeqIO.write([rec], sys.stdout, "genbank")




