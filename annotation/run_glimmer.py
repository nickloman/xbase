from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

import os, sys
import utils
import settings

if len(sys.argv) != 7:
    print "Usage: %s <working_dir> <reference> <sequence> <gene min length> <gene max overlap> <training-model>" % (sys.argv[0])
    raise SystemExit

working_dir = sys.argv[1]
reference_file = sys.argv[2]
sequence_file = sys.argv[3]
gene_min_length = int(sys.argv[4])
gene_max_overlap = int(sys.argv[5])
training_model = sys.argv[6]

GLIMMER_ARGS = "-o%s -g%s -t30"

# concatenate all the sequences
seq = ''
for rec in SeqIO.parse(open(reference_file), "fasta"):
    seq += rec.seq.tostring()

concat_reference_file = "%s/ref.concat.fna" % (working_dir)
rec = SeqRecord(id='concat_ref', description='concatenated reference file', seq=Seq(seq, IUPAC.ambiguous_dna))
SeqIO.write([rec], open(concat_reference_file, "w"), "fasta")

cmd = "%s/long-orfs -n -t 1.15 %s %s/ref.longorfs" % (settings.GLIMMER_PATH, concat_reference_file,  working_dir)
print cmd
os.system(cmd)

cmd = "%s/extract -t %s %s/ref.longorfs > %s/ref.train" % (settings.GLIMMER_PATH, concat_reference_file, working_dir, working_dir)
print cmd
os.system(cmd)

cmd = "%s/build-icm -r %s/ref.icm < %s/ref.train" % (settings.GLIMMER_PATH, working_dir, working_dir)
print cmd
os.system(cmd)

cmd = "%s/glimmer3 -o%d -g%d -t30 %s %s/ref.icm %s/seq" % (settings.GLIMMER_PATH, gene_max_overlap, gene_min_length, sequence_file, working_dir, working_dir)
print cmd
os.system(cmd)

print "Glimmer3 finished."


