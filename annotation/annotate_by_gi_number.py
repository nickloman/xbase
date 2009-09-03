#!/usr/bin/python

import sys, os, time
from Bio import SeqIO
from Bio import Entrez
from utils import add_qualifier

Entrez.email = "n.j.loman@bham.ac.uk"
terms = ["db_xref", "gene", "note", "product", "EC_number"]
consider_type = ["CDS", "gene", "Protein"]
DELAY = 0.3
BATCH_SIZE = 100
n = -1

def get_hash_from_record(record):
    hash = {}
    hash['match'] = record.annotations['organism']
    features = [feature for feature in record.features if feature.type in consider_type]
    try:
        for feature in features:
            for t in terms:
                if t in feature.qualifiers:
                    if t in hash:
                        feature.qualifiers[t].extend(hash[t])
                    else:
                        hash[t] = feature.qualifiers[t]
    except IndexError:
        pass
    return hash

for rec in SeqIO.parse(open(sys.argv[1]), "genbank"):
    print >>sys.stderr, "Processing %s" % (rec.id)

def lookup_batch(batch):
    results = {}
    print >>sys.stderr, "Retrieving batch of %s records" % (len(batch))
    x = ",".join([str(b) for b in batch])
    handle = Entrez.efetch(db="protein", id=x, rettype="gb")
    for rec in SeqIO.parse(handle, "genbank"):
        print >>sys.stderr, rec.annotations['gi']
        results[rec.annotations['gi']] = rec
    return results

def lookup_gi(gi):
    time.sleep(DELAY)
    print >>sys.stderr, "Looking up %s" % (gi)
    handle = Entrez.efetch(db="protein", id=gi, rettype="gb")
    record = SeqIO.read(handle, "genbank")
    print >>sys.stderr, record.annotations['organism']
    return get_hash_from_record(record)

for rec in SeqIO.parse(open(sys.argv[1]), "genbank"):
    print >>sys.stderr, "Processing %s" % (rec.id)

    lookup_list = []
    for feature in rec.features:
        if feature.type == 'CDS':
            if 'match' in feature.qualifiers:
                continue
            try:
                gi = feature.qualifiers['gi'][0]
                lookup_list.append(gi)
            except KeyError:
                pass

    results = {}
    while lookup_list:
        batch = []    
        try:
            for n in xrange(0,BATCH_SIZE):
                batch.append(lookup_list.pop())
        except IndexError:
            pass

        results.update(lookup_batch(batch))
        
    print >>sys.stderr, "Complete"
    for feature in rec.features:
        if feature.type == 'CDS':
            if 'match' in feature.qualifiers:
                continue
            try:
                gi = feature.qualifiers['gi'][0]
                qualifiers = get_hash_from_record(results[gi])
                for key, val in qualifiers.iteritems():
                    add_qualifier(feature, key, val)
            except KeyError:
                pass
    SeqIO.write([rec], sys.stdout, "genbank")

