import sys, os
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna, generic_protein

for rec in SeqIO.parse(sys.stdin, "genbank"):
	for feature in rec.features:
		if 'translation' not in feature.qualifiers:
			print >>sys.stderr, "Skipping %s as no translation" % (feature.qualifiers['locus_tag'][0])
			continue

		SeqIO.write([
			SeqRecord(
				Seq(feature.qualifiers['translation'][0], generic_protein),
				id="%s_%s" % (rec.id, feature.qualifiers['locus_tag'][0]),
				description=feature.qualifiers.get('product', [''])[0]
			)], sys.stdout, "fasta")

