#!/usr/bin/python

import sys, os, time
from Bio import SeqIO
from Bio import Entrez

from XBDB.models import SeqFeature, SeqFeatureQualifierValue, Annotation

from utils import add_qualifier

def get_hash_from_record(record):
    hash = {}
    #sfqv = SeqFeatureQualifierValue.objects.filter(seqfeature=record.seqfeature_id).order_by('rank').select_related('term')
    #for s in sfqv:
    #    if s.term.name in hash:
    #        hash[s.term.name].append(s.value)
    #    else:
    #        hash[s.term.name] = [s.value]
    #print hash

    a = Annotation.objects.filter(seqfeature=record.seqfeature_id)[0]

    return {
        'matching_locus_tag' : [a.locus_tag],
        'matching_protein_id' : [a.protein_id],
        'product' : [a.product]
    }


for rec in SeqIO.parse(open(sys.argv[1]), "genbank"):
    print >>sys.stderr, "Processing %s" % (rec.id)

    lookup_list = []
    for feature in rec.features:
        if feature.type == 'CDS':
            if 'match' in feature.qualifiers:
                continue
            try:
                seqfeature_id = feature.qualifiers['protein_id'][0]
                lookup_list.append(int(seqfeature_id))
            except KeyError:
                pass

    features = SeqFeature.objects.filter(pk__in=lookup_list)
    results = dict([(sf.seqfeature_id, sf) for sf in features])
    print >>sys.stderr, "Complete"

    for feature in rec.features:
        if feature.type == 'CDS':
            if 'match' in feature.qualifiers:
                continue
            try:
                seqfeature_id = int(feature.qualifiers['protein_id'][0])
                qualifiers = get_hash_from_record(results[seqfeature_id])
                for key, val in qualifiers.iteritems():
                    add_qualifier(feature, key, val)
            except KeyError:
                pass

    SeqIO.write([rec], sys.stdout, "genbank")

