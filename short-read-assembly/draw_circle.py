
from Bio.SeqFeature import SeqFeature, FeatureLocation
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio import SeqIO
import sys

record = SeqIO.read(open(sys.argv[1]), "genbank")
alignment_file = open(sys.argv[2])

gd_diagram = GenomeDiagram.Diagram("Mycobacterium tuberculosis Crown Hill")
gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
gd_feature_set = gd_track_for_features.new_set()

map_track1 = gd_diagram.new_track(2, name='track')
map_track2 = gd_diagram.new_track(3, name='track')
map_features = [map_track1.new_set(), map_track2.new_set()]

i = 0
for ln in alignment_file:
	cols = ln.rstrip().split("\t")
	try:
		length = int(cols[0])

		if int(cols[7]) > 100:
			print "Skipping %s with T gap %s" % (cols[9], cols[7])
			continue
		if cols[8] == '+':
			strand = +1
		else:
			strand = -1

		contig_name = " ".join(cols[9].split('_')[0:2])
		start = int(cols[15])
		end = int(cols[16])

		map_features[i].add_feature(SeqFeature(FeatureLocation(start, end), strand=strand), name=contig_name, label=True, label_size=6, label_angle=0)
		if i == 0:
			i = 1
		else:
			i = 0
	except ValueError:
		pass

draw_list = ['CDS', 'tRNA', 'rRNA']

i = 0
for feature in record.features:
    if feature.type not in draw_list:
    	continue
    if len(gd_feature_set) % 2 == 0 :
        color = colors.blue
    else :
        color = colors.lightblue
    if i % 20 == 0:
        label = False
    else:
        label = False
    gd_feature_set.add_feature(feature, sigil="ARROW", color="brown", arrowshaft_height=1.0, label=label, label_size=6, label_angle=0)
    i += 1

# gd_diagram.move_track(1,3)

gd_diagram.draw(format="linear",
#   circular=True,
   orientation="landscape",
   pagesize='A3',
   fragments=20,
   start=0,
   end=len(record))
gd_diagram.write("out.pdf", "PDF")
gd_diagram.write("out.eps", "EPS")
gd_diagram.write("out.svg", "SVG")
gd_diagram.write("out.png", "PNG")



