
import sys, os
from Bio.Blast import NCBIXML
from Bio import SeqIO
from utils import add_qualifier

if len(sys.argv) != 4:
    print "Usage: %s <Genbank File> <BLAST XML File> <threshold>" % (sys.argv[0])
    raise SystemExit

results = {}

class Result:
    def __init__(self, gi, protein_id, evalue):
        self.gi = gi
        self.protein_id = protein_id
        self.evalue = evalue

threshold = float(sys.argv[3])

blast_records = NCBIXML.parse(open(sys.argv[2]))
for blast_record in blast_records:
    record_id, sep, sequence_id = blast_record.query.split()[0].partition('_')
    if record_id not in results:
        results[record_id] = {}

    try:
        evalue = blast_record.descriptions[0].e
        if evalue > threshold:
            continue

        hit_def = blast_record.alignments[0].hit_def
        cols = hit_def.split('|')
        tag, gi, ignore, protein_id = cols[0:4]
        evalue = blast_record.descriptions[0].e
        results[record_id][sequence_id] = \
            Result(gi, protein_id, str(evalue))
    except IndexError, e:
        print "No results for %s" % (blast_record.query)

for rec in SeqIO.parse(open(sys.argv[1]), "genbank"):
    for feature in rec.features:
        if feature.type == 'CDS':
            locus_tag = feature.qualifiers['locus_tag'][0]

            try:
                add_qualifier(feature, 'gi', results[rec.id][locus_tag].gi)
                add_qualifier(feature, 'evalue', results[rec.id][locus_tag].evalue)
                add_qualifier(feature, 'protein_id', results[rec.id][locus_tag].protein_id)
            except KeyError, e:
                print >>sys.stderr, "** Skipping %s %s" % (rec.id, locus_tag)

    SeqIO.write([rec], sys.stdout, "genbank")

