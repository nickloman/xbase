#!/usr/bin/python

import sys, os

from SeqUtils import get_seq_0_based, bacterial_translate, translate_with_x
from Bio.Alphabet import IUPAC
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Data.CodonTable import TranslationError

for rec in SeqIO.parse(sys.stdin, "genbank"):
    for feature in rec.features:
        if feature.type == 'CDS':
            seq = get_seq_0_based(rec.seq.tostring(),
                feature.location.nofuzzy_start,
                feature.location.nofuzzy_end,
                feature.strand)
            seq = Seq(seq, IUPAC.ambiguous_dna)
            try:
#                translation = bacterial_translate(seq)
                translation = translate_with_x(seq, remove_stop=True)

                feature.qualifiers['translation'] = [translation.tostring()]
            except TranslationError, e:
                print >>sys.stderr, "skipping %s due to %s" % (feature.qualifiers['locus_tag'][0], e)

    SeqIO.write([rec], sys.stdout, "genbank")




