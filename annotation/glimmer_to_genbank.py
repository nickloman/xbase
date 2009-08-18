import sys, os
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.Alphabet import generic_dna

class Prediction:
	def __init__(self, sequence_id, cols):
		self.record_id = sequence_id
		self.cds_id = cols[0]
		self.start = int(cols[1])
		self.end = int(cols[2])
		self.frame = int(cols[3])
		self.raw_score = float(cols[4])

	@property
	def location(self):
		if self.start < self.end:
			start = self.start
			end = self.end
		else:
			start = self.end
			end = self.start
		return FeatureLocation(start=start-1, end=end)

	@property
	def strand(self):
		assert(self.frame != 0)
		if self.frame < 0:
			return -1
		elif self.frame > 0:
			return 1

def read_predictions(fh):
	predictions = {}
	identifier = None
	for ln in fh:
		ln = ln.rstrip()
		if ln.startswith('>'):
			record_id = ln[1:]
			truncated_id = record_id.split()[0]
			if truncated_id != record_id:
				print >>sys.stderr, "Truncating id to %s" % (truncated_id,)
				record_id = truncated_id
			predictions[record_id] = []
		else:
			cols = ln.split()
			predictions[record_id].append(
				Prediction(record_id, cols)
			)
	return predictions

def attach_features(predictions, seqrecord):
	for prediction in predictions[seqrecord.id]:
		if prediction.raw_score >= 1.0:
			qualifiers = {}
			qualifiers['locus_tag'] = [prediction.cds_id]
			feature = SeqFeature(
				location=prediction.location,
				type='CDS',
				strand=prediction.strand,
				qualifiers=qualifiers,
			)
			feature.qualifiers = qualifiers
			seqrecord.features.append(feature)

if len(sys.argv) != 3:
	print "Usage: %s <FASTA File> <Glimmer Prediction File>" % (sys.argv[0])
	raise SystemExit

predictions = read_predictions(open(sys.argv[2]))

for rec in SeqIO.parse(open(sys.argv[1]), "fasta", generic_dna):
	attach_features(predictions, rec)
	rec.name = rec.id[0:15]
	SeqIO.write([rec], sys.stdout, "genbank")

