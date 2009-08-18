import sys, os
from Bio import SeqIO
from Bio.SeqFeature import ExactPosition, FeatureLocation

for rec in SeqIO.parse(open(sys.argv[1]), "genbank"):
	for feature in rec.features:
		feature.location = FeatureLocation(
			ExactPosition(feature.location.nofuzzy_start - 1),
			ExactPosition(feature.location.nofuzzy_end)
		)
	SeqIO.write([rec], sys.stdout, "genbank")

